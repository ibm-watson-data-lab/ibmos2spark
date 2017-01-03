# ibmos2spark

The package configures Spark Hadoop configurations for connecting to 
Softlayer and IBM Bluemix Object Stores with the 'swift' or 'swift2d' protocol. 

It is recommended to use 'swift2d' instead of the previous version. 
The new version allows for more flexible names (underscores) and is faster.

### Installation 
library(devtools)

devtools::install_url("https://github.com/ibm-cds-labs/ibmos2spark/archive/adding_r_scala_platform.zip", subdir= "r")
### Softlayer

#### Using Swift (version 1) Driver
library(ibmos2spark)
slsc = softlayer(sparkcontext=sc, 
                 name="XXXXX", 
                 auth_url="https://identity.open.softlayer.com",
                 region="XXXXX", 
                 tenant = "XXXXX", 
                 username="XXXXX", 
                 password="XXXXX"
           )
           
data <- read.df(sqlContext, slsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
head(data)


#### Using Swift2d Driver

library(ibmos2spark)
slsc = softlayer2d(sparkcontext=sc, 
                 name="XXXXX", 
                 auth_url="https://identity.open.softlayer.com",
                 region="XXXXX", 
                 tenant = "XXXXX", 
                 username="XXXXX", 
                 password="XXXXX"
           )
           
data <- read.df(sqlContext, slsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
head(data)

### Bluemix

#### Using Swift Driver

library(ibmos2spark)
creds = list(name="XXXXX", 
             auth_url="https://identity.open.softlayer.com",
            region="dallas", 
            project_id = "XXXXX", 
            user_id="XXXXX", 
            password="XXXXX",
            public = FALSE)
            
bmsc = bluemix(sparkcontext=sc, name=name, credentials = creds)

data <- read.df(sqlContext, bmsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
head(data)


#### Using Swift2d Driver

library(ibmos2spark)
creds = list(name="XXXXX", 
             auth_url="https://identity.open.softlayer.com",
            region="dallas", 
            project_id = "XXXXX", 
            user_id="XXXXX", 
            password="XXXXX",
            public = FALSE)
            
bmsc = bluemix2d(sparkcontext=sc, name=name, credentials = creds)

data <- read.df(sqlContext, bmsc$url(name, space,object), source = "com.databricks.spark.csv", header = "true")
head(data)


### License 

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
