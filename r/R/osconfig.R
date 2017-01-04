
setOldClass("jobj")


swifturl = function(name, container_name, object_name){
  if ( grepl('_',name)){
    stop(paste0('The swift protocol does not support underscores (_) in "name" ', paste0(name)))
  }
  if (grepl('_',container_name)){
    stop(paste0('The swift protocol does not support underscores (_) in "container" ', paste0(container_name),'. Instead use swift2d via softlayer2d or bluemix2d objects.'))
  }
  return(paste0('swift://',container_name,'.',name,'/',object_name))
}


swifturl2d = function(name, container_name, object_name){
  return(paste0('swift2d://',container_name,'.',name,'/',object_name))
}


#'    sparkcontext is a SparkContext object.
#' 
#'    name is a string that identifies this configuration. You can
#'        use any string you like. This allows you to create
#'        multiple configurations to different Object Storage accounts.
#'
#'    auth_url, username and password are string credentials for your
#'    Softlayer Object Store
#' @export softlayer      
#' @exportClass softlayer
#' @examples
#' library(ibmos2spark)
#' slsc = softlayer2d(sparkcontext=sc, 
#'                  name="XXXXX", 
#'                  auth_url="https://identity.open.softlayer.com",
#'                  region="XXXXX", 
#'                  tenant = "XXXXX", 
#'                  username="XXXXX", 
#'                  password="XXXXX"
#'            )
#'            
#' data <- read.df(sqlContext, slsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
#' head(data)

    
softlayer <- setRefClass("softlayer",
  fields=list(name="character", container_name="character", object_name="character",
             sparkcontext='jobj', auth_url="character", region="character", 
              tenant = "character", username="character", password="character"),
  methods=list(initialize = 
    function( sparkcontext, name, auth_url, region, tenant, username, password,public=FALSE){     

      if ( grepl('_',name)){
        stop(paste0('The swift protocol does not support underscores (_) in "name" ', paste0(name)))
      }

        prefix = paste("fs.swift.service" , name, sep =".")
        hConf = SparkR:::callJMethod(sparkcontext, "hadoopConfiguration")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.url", sep='.'), paste(auth_url,"/v3/auth/tokens",sep=""))
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "tenant", sep='.'), tenant)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "username", sep='.'), username)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "password", sep='.'), password)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "region", sep='.'), region)
        invisible(SparkR:::callJMethod(hConf, "setBoolean", paste(prefix, "public", sep='.'), TRUE))},

        url = function(name, container_name, object_name){
        return(swifturl(name, container_name, object_name))}
    )
)


#' sparkcontext is a SparkContext object.
#' 
#' name is a string that identifies this configuration. You can
#'     use any string you like. This allows you to create
#'     multiple configurations to different Object Storage accounts.
#' auth_url, username and password are string credentials for your
#' Softlayer Object Store
#' @export softlayer2d        
#' @exportClass softlayer2d
#' @examples 
#' library(ibmos2spark)
#' slsc = softlayer2d(sparkcontext=sc, 
#'                  name="XXXXX", 
#'                  auth_url="https://identity.open.softlayer.com",
#'                  region="XXXXX", 
#'                  tenant = "XXXXX", 
#'                  username="XXXXX", 
#'                  password="XXXXX"
#'            )
#'            
#' data <- read.df(sqlContext, slsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
#' head(data)

softlayer2d <- setRefClass("softlayer2d",
  fields=list(name="character", container_name="character", object_name="character",
             sparkcontext='jobj', auth_url="character", region="character", 
              tenant = "character", username="character", password="character"),
  methods=list(initialize = 
    function( sparkcontext, name, auth_url, region, tenant, username, password,public=FALSE,
              swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'){     


        prefix = paste("fs.swift2d.service" , name, sep =".")
        hConf = SparkR:::callJMethod(sparkcontext, "hadoopConfiguration")
        SparkR:::callJMethod(hConf, "set", "fs.swift2d.impl", swift2d_driver)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.url", sep='.'), paste(auth_url,"/v3/auth/tokens",sep=""))
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "tenant", sep='.'), tenant)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "username", sep='.'), username)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "password", sep='.'), password)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.method", sep='.'), "keystoneV3")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "region", sep='.'), region)
        invisible(SparkR:::callJMethod(hConf, "setBoolean", paste(prefix, "public", sep='.'), public))

        #invisible(SparkR:::callJMethod(hConf, "setInt", paste(prefix, "http.port", sep='.'), 8080))
    },

        url = function(name, container_name, object_name){
        return(swifturl2d(name, container_name, object_name))}
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
#' 
#' @examples 
#' library(ibmos2spark)
#' creds = list(name="XXXXX", 
#'              auth_url="https://identity.open.softlayer.com",
#'             region="dallas", 
#'             project_id = "XXXXX", 
#'             user_id="XXXXX", 
#'             password="XXXXX",
#'             public = FALSE)
#'             
#' bmsc = bluemix(sparkcontext=sc, name=name, credentials = creds)
#' 
#' data <- read.df(sqlContext, bmsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
#' head(data)


bluemix <- setRefClass("bluemix",
  fields=list(name="character", credentials = "list", 
             sparkcontext='jobj', public = "character"),
  methods=list(initialize = 
    function(..., sparkcontext, name=NULL, credentials,public=FALSE){     

       callSuper(...,credentials=credentials)

      if ( is.null(name)) name <<- credentials["name"][[1]]
          
      if ( grepl('_',name)){
        stop(paste0('The swift protocol does not support underscores (_) in "name" ', paste0(name)))
      }
          
      user_id = try( credentials['user_id'][[1]])
      if(class(user_id)=="try-error")  user_id = credentials['userId'][[1]]
          
      tenant = try( credentials['project_id'][[1]])
      if(class(tenant)=="try-error")  tenant = credentials['projectId'][[1]]


        prefix = paste("fs.swift.service" , name, sep =".")
        hConf = SparkR:::callJMethod(sparkcontext, "hadoopConfiguration")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.url", sep='.'), paste(credentials['auth_url'][[1]],"/v3/auth/tokens",sep=""))
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "tenant", sep='.'), tenant)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "username", sep='.'), user_id)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "password", sep='.'), credentials['password'][[1]])
        SparkR:::callJMethod(hConf, "set", paste(prefix, "region", sep='.'), credentials['region'][[1]])
        invisible(SparkR:::callJMethod(hConf, "setBoolean", paste(prefix, "public", sep='.'), credentials['public'][[1]]))},

        url = function(name, container_name, object_name){
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
#' @export bluemix2d        
#' @exportClass bluemix2d
#' @examples 
#' library(ibmos2spark)
#' creds = list(name="XXXXX", 
#'              auth_url="https://identity.open.softlayer.com",
#'             region="dallas", 
#'             project_id = "XXXXX", 
#'             user_id="XXXXX", 
#'             password="XXXXX",
#'             public = FALSE)
#'             
#' bmsc = bluemix(sparkcontext=sc, name=name, credentials = creds)
#' 
#' data <- read.df(sqlContext, bmsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
#' head(data)

          
bluemix2d <- setRefClass("bluemix2d",
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
          
        prefix = paste("fs.swift2d.service" , name, sep =".")
        hConf = SparkR:::callJMethod(sparkcontext, "hadoopConfiguration")
        SparkR:::callJMethod(hConf, "set", "fs.swift2d.impl", swift2d_driver)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.url", sep='.'), paste(credentials['auth_url'][[1]],"/v3/auth/tokens",sep=""))
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.endpoint.prefix", sep='.'), "endpoints")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "tenant", sep='.'), tenant)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "username", sep='.'), user_id)
        SparkR:::callJMethod(hConf, "set", paste(prefix, "password", sep='.'), credentials['password'][[1]])
        SparkR:::callJMethod(hConf, "set", paste(prefix, "auth.method", sep='.'), "keystoneV3")
        SparkR:::callJMethod(hConf, "set", paste(prefix, "region", sep='.'), credentials['region'][[1]])
        invisible(SparkR:::callJMethod(hConf, "setBoolean", paste(prefix, "public", sep='.'), credentials['public'][[1]]))
        #invisible(SparkR:::callJMethod(hConf, "setInt", paste(prefix, "http.port", sep='.'), 8080))
          },
          
        url = function(name, container_name, object_name){
        return(swifturl2d(name, container_name, object_name))}
    )
)
