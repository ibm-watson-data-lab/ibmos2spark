# ibmos2sparkR

The package sets Spark Hadoop configurations for connecting to
IBM Bluemix Object Storage and Softlayer Account Object Storage instances. This packages uses the new [stocator](https://github.com/SparkTC/stocator) driver, which implements the `swift2d` protocol, and is availble
on the latest IBM Apache Spark Service instances (and through IBM Data Science Experience).

Using the `stocator` driver connects your Spark executor nodes directly
to your data in object storage.
This is an optimized, high-performance method to connect Spark to your data. All IBM Apache Spark kernels
are instantiated with the `stocator` driver in the Spark kernel's classpath.
You can also run this locally by installing the [stocator driver](https://github.com/SparkTC/stocator)
and adding it to your local Apache Spark kernel's classpath.


This package expects a SparkContext instantiated by SparkR. It has been tested to work with
IBM Spark service in R notebooks on IBM DSX, though it should work with other Spark installations
that utilize the [swift2d/stocator](https://github.com/SparkTC/stocator) protocol.


## Installation

    library(devtools)
    devtools::install_url("https://github.com/ibm-cds-labs/ibmos2spark/archive/<version).zip", subdir= "r/sparkr/")

where `version` should be a tagged release, such as `0.0.7`. (If you're daring, you can use `master`.)

## Usage

The usage of this package depends on *from where* your Object Storage instance was created. This package
is intended to connect to IBM's Object Storage instances obtained from Bluemix or Data Science Experience
(DSX) or from a separate account on IBM Softlayer. It also supports IBM cloud object storage (COS). The
instructions below show how to connect to either type of instance.

The connection setup is essentially the same. But the difference for you is how you deliver the
credentials. If your Object Storage was created with Bluemix/DSX, with a few clicks on the side-tab
within a DSX Jupyter notebook, you can obtain your account credentials in the form of a list.
If your Object Storage was created with a Softlayer account, each part of the credentials will
be found as text that you can copy and paste into the example code below.

### Cloud Object Storage
    library(ibmos2sparkR)
    configurationName = "bluemixO123"

    # In DSX notebooks, the "insert to code" will insert this credentials list for you
    credentials <- list(
      accessKey = "123",
      secretKey = "123",
      endpoint = "https://s3-api.objectstorage.....net/"
    )

    cos <- CloudObjectStorage(sparkContext=sc, credentials=credentials, configurationName=configurationName)
    bucketName <- "bucketName"
    fileName <- "test.csv"
    url <- cos$url(bucketName, fileName)

    invisible(sparkR.session(appName = "SparkSession R"))

    df.data.1 <- read.df(url,
        source = "org.apache.spark.sql.execution.datasources.csv.CSVFileFormat",
        header = "true")
    head(df.data.1)


### Bluemix / Data Science Experience

    library(ibmos2sparkR)
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

    # OR, for Spark >= 2.0.0

    data = read.df(bmconfig$url(container, objectname), source="com.databricks.spark.csv", header="true")


### Softlayer

    library(ibmos2sparkR)
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

    # OR, for Spark >= 2.0.0

    data = read.df(slconfig$url(container, objectname), source="com.databricks.spark.csv", header="true")

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
