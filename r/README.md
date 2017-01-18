# ibmos2spark

The package sets Spark Hadoop configurations for connecting to 
Softlayer and IBM Bluemix Object Stores with the swift protocol. This packages
uses the new 'swift2d' protocol. 

## Installation 
    library(devtools)
    devtools::install_url("https://github.com/ibm-cds-labs/ibmos2spark/archive/master.zip", subdir= "r")

## Usage

### Softlayer

    library(ibmos2spark)
    configurationname = "softlayerOScon" #can be any any name you like (allows for multiple configurations)

    slconfig = softlayer(sparkcontext=sc, 
                 name=configurationname, 
                 auth_url="https://identity.open.softlayer.com",
                 tenant = "XXXXX", 
                 username="XXXXX", 
                 password="XXXXX"
           )
           
    container = "my_container"
    object = "my_data.csv"

    data <- read.df(sqlContext, slconfig$url(container,object), source = "com.databricks.spark.csv", header = "true")
    head(data)

### Bluemix

    library(ibmos2spark)
    configurationname = "bluemixOScon" #can be any any name you like (allows for multiple configurations)

    # In DSX notebooks, the "insert to code" will insert this credentials list for you
    creds = list(
            auth_url="https://identity.open.softlayer.com",
            region="dallas", 
            project_id = "XXXXX", 
            user_id="XXXXX", 
            password="XXXXX")
            
    bmconfig = bluemix(sparkcontext=sc, name=configurationname, credentials = creds)

    container = "my_container"
    object = "my_data.csv"

    data <- read.df(sqlContext, bmconfig$url(container,object), source = "com.databricks.spark.csv", header = "true")
    head(data)


## License 

Copyright 2016 IBM Cloud Data Services

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
