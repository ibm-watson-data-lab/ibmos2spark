setOldClass("jobj")


swifturl = function(name, container_name, object_name){
  return(paste0('swift2d://',container_name,'.',name,'/',object_name))
}



#' sparkcontext is a SparkContext object.
#'
#' name is a string that identifies this configuration. You can
#'     use any string you like. This allows you to create
#'     multiple configurations to different Object Storage accounts.
#' auth_url, username and password are string credentials for your
#' Softlayer Object Store
#' @export softlayer
#' @exportClass softlayer

softlayer <- setRefClass("softlayer",
  fields=list(name="character", container_name="character", object_name="character",
             sparkcontext='jobj', auth_url="character",
              tenant = "character", username="character", password="character"),
  methods=list(initialize =
    function( sparkcontext, name, auth_url, tenant, username, password,public=FALSE,
              swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'){

        .self$name = name
        # get spark_context
        ctx <- spark_context(sparkcontext)

        #set the java spark context
        jsc <- invoke_static(
          sparkcontext,
          "org.apache.spark.api.java.JavaSparkContext",
          "fromSparkContext",
          ctx
        )

        #set the swift configs:
        prefix = paste("fs.swift2d.service" , name, sep =".")
        hconf = jsc %>% invoke("hadoopConfiguration")
        hconf %>% invoke("set", "fs.swift2d.impl", swift2d_driver)
        hconf %>% invoke("set", paste(prefix, "auth.url", sep='.'), auth_url)
        hconf %>% invoke("set", paste(prefix, "username", sep='.'), username)
        hconf %>% invoke("set", paste(prefix, "tenant", sep='.'), tenant)
        hconf %>% invoke("set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        hconf %>% invoke("set", paste(prefix, "auth.method", sep='.'), "swiftauth")
        hconf %>% invoke("set", paste(prefix, "http.port", sep='.'), "8080")
        hconf %>% invoke("set", paste(prefix, "apikey", sep='.'), password)
        invisible(hconf %>% invoke("setBoolean", paste(prefix, "public", sep='.'), public))
        hconf %>% invoke("set", paste(prefix, "use.get.auth", sep='.'), "true")
        invisible(hconf %>% invoke("setBoolean", paste(prefix, "location-aware", sep='.'), FALSE))
        hconf %>% invoke("set", paste(prefix, "password", sep='.'), password)



    },

        url = function(container_name, object_name){
        return(swifturl(name, container_name, object_name))}
    )
)



#' sparkcontext:  a SparkContext object.
#'
#' credentials:  a dictionary with the following required keys:
#'
#'   auth_url
#'   project_id (or projectId)
#'   user_id (or userId)
#'   password
#'   region
#' and optional key:
#'   name  #[to be deprecated] The name of the configuration.
#' name:  string that identifies this configuration. You can
#'     use any string you like. This allows you to create
#'     multiple configurations to different Object Storage accounts.
#'     This is not required at the moment, since credentials['name']
#'     is still supported.
#' When using this from a IBM Spark service instance that
#' is configured to connect to particular Bluemix object store
#' instances, the values for these credentials can be obtained
#' by clicking on the 'insert to code' link just below a data
#' source.
#' @export bluemix
#' @exportClass bluemix


bluemix <- setRefClass("bluemix",
  fields=list(name="character", credentials = "list",
             sparkcontext='jobj', public = "character"),
  methods=list(initialize =
    function(..., sparkcontext, name=NULL, credentials,
             public=FALSE,swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'){

      callSuper(...,credentials=credentials)

      if ( is.null(name)) name <<- credentials["name"][[1]]

      user_id = try( credentials['user_id'][[1]])
      if(class(user_id)=="try-error")  user_id = credentials['userId'][[1]]

      tenant = try( credentials['project_id'][[1]])
      if(class(tenant)=="try-error")  tenant = credentials['projectId'][[1]]

        .self$name = name
        # get spark_context
        ctx <- spark_context(sparkcontext)

        #set the java spark context
        jsc <- invoke_static(
          sparkcontext,
          "org.apache.spark.api.java.JavaSparkContext",
          "fromSparkContext",
          ctx
        )

        #set the swift configs:
        prefix = paste("fs.swift2d.service" , name, sep =".")
        hconf = jsc %>% invoke("hadoopConfiguration")
        hconf %>% invoke("set", "fs.swift2d.impl", swift2d_driver)
        hconf %>% invoke("set", paste(prefix, "auth.url", sep='.'), paste(credentials['auth_url'][[1]],"/v3/auth/tokens",sep=""))
        hconf %>% invoke("set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        hconf %>% invoke("set", paste(prefix, "tenant", sep='.'), tenant)
        hconf %>% invoke("set", paste(prefix, "username", sep='.'), user_id)
        hconf %>% invoke("set", paste(prefix, "password", sep='.'), credentials['password'][[1]])
        hconf %>% invoke("set", paste(prefix, "auth.method", sep='.'), "keystoneV3")
        hconf %>% invoke("set", paste(prefix, "region", sep='.'), credentials['region'][[1]])
        invisible(hconf %>% invoke("setBoolean", paste(prefix, "public", sep='.'), public))
        #invisible(SparkR:::callJMethod(hConf, "setInt", paste(prefix, "http.port", sep='.'), 8080))
          },

        url = function( container_name, object_name){
        return(swifturl(name, container_name, object_name))}
    )
)
