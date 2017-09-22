package com.ibm.ibmos2spark

import scala.collection.mutable.HashMap
import org.apache.spark.SparkContext

val DEFAULT_SERVICE_NAME = "service"

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
* CloudObjectStorage class sets up a s3d connection between an IBM Spark service
* instance and an IBM Cloud Object Storage instance.

* Constructor arguments:

*   sparkcontext:  a SparkContext object.

*   credentials:  a dictionary with the following required keys:
*
*     endpoint

*     accessKey

*     secretKey

*    cosId [optional]: this parameter is the cloud object storage unique id. It is useful
            to keep in the class instance for further checks after the initialization. However,
            it is not mandatory for the class instance to work. This value can be retrieved by
            calling the getCosId function.

    bucket_name (projectId in DSX) [optional]:  string that identifies the defult
             bucket nameyou want to access files from in the COS service instance.
             In DSX, bucket_name is the same as projectId. One bucket is
             associated with one project.
             If this value is not specified, you need to pass it when
             you use the url function.
*
    Warning: creating a new instance of this class would overwrite the existing
              spark hadoop configs if set before if used with the same spark context instance.
*/
class CloudObjectStorage(sc: SparkContext, credentials: HashMap[String, String], configurationName: String = "") {

    // check if all credentials are available
    val requiredValues = Array("endPoint", "accessKey", "secretKey")
    for ( key <- requiredValues ) {
        if (!credentials.contains(key)) {
            throw new IllegalArgumentException("Invalid input: missing required input [" + key + "]")
        }
    }

    // set config
    val hadoopConf = sc.hadoopConfiguration
    val prefix = "fs.cos." + getConfigurationName()

    hadoopConf.set(prefix + ".endpoint", credentials("endPoint"))
    hadoopConf.set(prefix + ".access.key", credentials("accessKey"))
    hadoopConf.set(prefix + ".secret.key", credentials("secretKey"))

    private def getConfigurationName() : String = {
      if (configurationName != "") {
        return configurationName
      } else {
        return DEFAULT_SERVICE_NAME
      }
    }

    def url(bucketName: String, objectName: String) : String = {
      var serviceName = getConfigurationName()
      return "cos://" + bucketName + "." + serviceName + "/" + objectName
    }
}
