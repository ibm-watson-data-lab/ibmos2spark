% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/osconfig.R
\docType{class}
\name{CloudObjectStorage-class}
\alias{CloudObjectStorage}
\alias{CloudObjectStorage-class}
\title{CloudObjectStorage is a class that is designed for IBM cloud object storage (COS)
It sets up the hadoop config for COS and provide the final file url. It also supports
 connecting to an IBM COS instance that is being hosted on bluemix.}
\description{
sparkContext:  a SparkContext object.
'
credentials:  a dictionary with the required keys to connect to an IBM cloud object storage.
  The required keys differ according to the type of COS.
    - for COS type "softlayer_cos" the following keys are required:
        endpoint [required]
        accessKey [required]
        secretKey [required]
    - for COS type "bluemix_cos", here are the required/optional key:
        endPoint [required]
        serviceId [required]
        apiKey OR iamToken depends on the selected authorization method (authMethod) [required]
        iamServiceEndpoint [optional] (default: https://iam.ng.bluemix.net/oidc/token)
        v2SignerType [optional]
}
\details{
configurationName: string identifies the configurations to be set.

cosType [optional]: string that identifies the type of COS to connect to. The supported types of COS
   are "softlayer_cos" and "bluemix_cos". "softlayer_cos" will be chosen as default if no cosType is passed.

authMethod [optional]: string that identifies the type of authorization method to use when connecting to COS. This parameter
   is not reqired for softlayer_cos but only needed for bluemix_cos. Two options can be chosen for this params
   "api_key" or "iam_token". "api_key" will be chosen as default if the value is not set.
}
