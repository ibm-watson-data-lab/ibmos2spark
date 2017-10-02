package com.ibm.ibmos2spark

import scala.collection.mutable.HashMap
import org.apache.spark.SparkContext

object globalVariables {
  val DEFAULT_SERVICE_NAME = "service"
}


object urlbuilder{
  def swifturl2d(name: String, container_name: String, object_name: String): String = {
   return "swift2d://" + container_name  + "." + name + "/" + object_name
  }
}

/**
* softlayer class sets up a swift connection between an IBM Spark service
* instance and Softlayer Object Storgae instance.
*
* Constructor arguments

*    sparkcontext: a SparkContext object.
*
*    name: string that identifies this configuration. You can
*      use any string you like. This allows you to create
*      multiple configurations to different Object Storage accounts.
*
*    auth_url, tenant, username and password:  string credentials for your
*      Softlayer Object Store
*/

class softlayer(sc: SparkContext, name: String, auth_url: String,
                  tenant: String, username: String, password: String,
                  swift2d_driver: String = "com.ibm.stocator.fs.ObjectStoreFileSystem",
                  public: Boolean=false){


    val hadoopConf = sc.hadoopConfiguration;
    val prefix = "fs.swift2d.service." + name

    hadoopConf.set("fs.swift2d.impl",swift2d_driver)
    hadoopConf.set(prefix + ".auth.url",auth_url)
    hadoopConf.set(prefix + ".username", username)
    hadoopConf.set(prefix + ".tenant", tenant)
    hadoopConf.set(prefix + ".auth.endpoint.prefix","endpoints")
    hadoopConf.set(prefix + ".auth.method","swiftauth")
    hadoopConf.setInt(prefix + ".http.port",8080)
    hadoopConf.set(prefix + ".apikey",password)
    hadoopConf.setBoolean(prefix + ".public",public)
    hadoopConf.set(prefix + ".use.get.auth","true")
    hadoopConf.setBoolean(prefix + ".location-aware",false)
    hadoopConf.set(prefix + ".password",password)


    def url(container_name: String, object_name:String) : String= {
        return(urlbuilder.swifturl2d(name= name, container_name,object_name))
    }
}

/**
* bluemix class sets up a swift connection between an IBM Spark service
* instance and an Object Storage instance provisioned through IBM Bluemix.

* Constructor arguments:

*   sparkcontext:  a SparkContext object.

*   credentials:  a dictionary with the following required keys:
*
*     auth_url

*     project_id (or projectId)

*     user_id (or userId)

*     password

*     region
*
*   name:  string that identifies this configuration. You can
*     use any string you like. This allows you to create
*     multiple configurations to different Object Storage accounts.
*     This is not required at the moment, since credentials['name']
*     is still supported.
*
* When using this from a IBM Spark service instance that
* is configured to connect to particular Bluemix object store
* instances, the values for these credentials can be obtained
* by clicking on the 'insert to code' link just below a data
* source.
*/

class bluemix(sc: SparkContext, name: String, creds: HashMap[String, String],
                swift2d_driver: String = "com.ibm.stocator.fs.ObjectStoreFileSystem",
                public: Boolean =false){


    def ifexist(credsin: HashMap[String, String], var1: String, var2: String): String = {
        if (credsin.keySet.exists(_ == var1)){
            return(credsin(var1))
        }else {
           return(credsin(var2))
        }
    }

    val username = ifexist(creds, "user_id","userId")
    val tenant = ifexist(creds, "project_id","projectId")


    val hadoopConf = sc.hadoopConfiguration;
    val prefix = "fs.swift2d.service." + name;

    hadoopConf.set("fs.swift2d.impl",swift2d_driver)

    hadoopConf.set(prefix + ".auth.url",creds("auth_url") + "/v3/auth/tokens")
    hadoopConf.set(prefix + ".auth.endpoint.prefix","endpoints")
    hadoopConf.set(prefix + ".auth.method","keystoneV3")
    hadoopConf.set(prefix + ".tenant",tenant)
    hadoopConf.set(prefix + ".username",username)
    hadoopConf.set(prefix + ".password",creds("password"))
    hadoopConf.setBoolean(prefix + ".public",public)
    hadoopConf.set(prefix + ".region",creds("region"))
    hadoopConf.setInt(prefix + ".http.port",8080)

    def url(container_name: String, object_name:String) : String= {
        return(urlbuilder.swifturl2d(name= name, container_name,object_name))
    }
}

/**
*  This class allows you to connect to a cloud object storage (COS) instance. It also support
    connecting to a cos instance that is being hosted on bluemix.

* Constructor arguments:

*   sparkcontext:  a SparkContext object.

*   credentials:  a dictionary with the following required keys to connect to cos.
      The required keys differ according to the type of cos.
*      - for cos type "softlayer_cos" the following key are required:
          * endpoint [required]
          * accessKey [required]
          * secretKey [required]
*      - for cos type "bluemix_cos", here are the required/optional key:
          * endpoint [required]
          * serviceId [required]
          * apiKey OR iamToken depends on the selected authorization method (authMethod) [required]
          * iamServiceEndpoint [optional] (default: https://iam.ng.bluemix.net/oidc/token)
          * v2SignerType [optional]

*   configurationName [optional]: string that identifies this configuration. You can
            use any string you like. This allows you to create
            multiple configurations to different Object Storage accounts.
            if a configuration name is not passed the default one will be used "service".

*   cosType [optional]: string that identifies the type of cos to connect to. The supported types of cos
            are "softlayer_cos" and "bluemix_cos". "softlayer_cos" will be chosen as default if no cosType is passed.

*   authMethod [optional]: string that identifies the type of authorization method to use when connecting to cos. This parameter
            is not reqired for softlayer_cos but only needed for bluemix_cos. Two options can be chosen for this params
            "api_key" or "iam_token". "api_key" will be chosen as default if the value is not set.
*/
class CloudObjectStorage(sc: SparkContext, credentials: HashMap[String, String],
                         configurationName: String = "", cosType="softlayer_cos",
                         authMethod="api_key") {

    // check for valid credentials
    _validate_credentials(credentials, cosType, authMethod)

    // set config
    val hadoopConf = sc.hadoopConfiguration
    val prefix = "fs.cos." + _getConfigurationName()

    hadoopConf.set(prefix + ".endpoint", credentials("endPoint"))

    if (cos_type == "softlayer_cos") {
      // softlayer cos case
      hadoopConf.set(prefix + ".access.key", credentials("accessKey"))
      hadoopConf.set(prefix + ".secret.key", credentials("secretKey"))
    } else if (cos_type == "bluemix_cos") {
      // bluemix cos case
      hadoopConf.set(prefix + ".iam.service.id", credentials("serviceId"))
      if (authMethod == "api_key") {
        hadoopConf.set(prefix + ".iam.api.key", credentials("apiKey"))
      } else if (authMethod == "iam_token") {
        hadoopConf.set(prefix + ".iam.token", credentials("iamToken"))
      }

      if (credentials.contains("iamServiceEndpoint")) {
        hadoopConf.set(prefix + ".iam.endpoint", credentials("iamServiceEndpoint"))
      }

      if (credentials.contains("v2SignerType")) {
        hadoopConf.set(prefix + ".v2.signer.type", credentials("v2SignerType"))
      }
    }

    private def _getConfigurationName() : String = {
      if (configurationName != "") {
        return configurationName
      } else {
        return globalVariables.DEFAULT_SERVICE_NAME
      }
    }

    private def _validate_credentials(credentials, cosType, authMethod) {
      val requiredKeys = _get_required_key_array(cosType, authMethod)

      // check the existence of all required values in credentials
      for ( key <- requiredKeys ) {
          if (!credentials.contains(key)) {
              throw new IllegalArgumentException("Invalid input: missing required input [" + key + "]")
          }
      }
    }

    private def _get_required_key_array(cosType, authMethod) : Array {
      val required_key_softlayer_cos = Array("endPoint", "accessKey", "secretKey")
      val required_key_list_iam_api_key = Array("endPoint", "apiKey", "serviceId")
      val required_key_list_iam_token = Array("endPoint", "iamToken", "serviceId")

      if (cosType == "bluemix_cos") {
        if (authMethod == "api_key") {
          return required_key_list_iam_api_key
        } else if (authMethod == "iam_token") {
          return required_key_list_iam_token
        } else {
          throw new IllegalArgumentException("Invalid input: authMethod. authMethod is optional but if set, it should have one of the following values: api_key, iam_token")
        }
      } else if (cosType == "softlayer_cos") {
        return required_key_softlayer_cos
      } else {
        throw new IllegalArgumentException("Invalid input: cosType. cosType is optional but if set, it should have one of the following values: softlayer_cos, bluemix_cos")
      }
    }

    def url(bucketName: String, objectName: String) : String = {
      var serviceName = _getConfigurationName()
      return "cos://" + bucketName + "." + serviceName + "/" + objectName
    }
}
