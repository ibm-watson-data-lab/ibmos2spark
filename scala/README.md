# ibmos2spark

The `ibmos2park` library facilitates data read/write connections between Apache Spark clusters and the various 
[IBM Object Storage services](https://console.bluemix.net/catalog/infrastructure/object-storage-group). 

![IBM Object Storage Services](fig/ibm_objectstores.png "IBM Object Storage Services")

### Object Storage Documentation

* [Cloud Object Storage](https://www.bluemix.net/docs/services/cloud-object-storage/getting-started.html)
* [Cloud Object Storage (IaaS)](https://ibm-public-cos.github.io/crs-docs/)
* [Object Storage OpenStack Swift (IaaS)](https://ibm-public-cos.github.io/crs-docs/)
* [Object Storage OpenStack Swift for Bluemix](https://www.ng.bluemix.net/docs/services/ObjectStorage/index.html)



## Requirements

* Apache Spark with `stocator` library

The easiest way to install the `stocator` library with Apache Spark is to 
[pass the Maven coordinates at launch](https://spark-packages.org/package/SparkTC/stocator).
Other installation options are described in the [`stocator` documentation](https://github.com/SparkTC/stocator).

## Installation

This library is cross-built on both Scala 2.10 (for Spark 1.6.0) and Scala 2.11 (for Spark 2.0.0 and greater)

### Apache Spark at IBM

The `stocator` and `ibmos2spark` libraries are pre-installled and available on 

* [Apache Spark through IBM Bluemix](https://console.bluemix.net/catalog/services/apache-spark)
* [IBM Analytics Engine (Beta)](https://console.bluemix.net/catalog/services/ibm-analytics-engine)  
* [IBM Data Science Experience](https://datascience.ibm.com)


### Version Releases

#### SBT library dependency

```
"com.ibm.ibmos2spark" %% "ibmos2spark" % "0.0.9"
```

#### Maven Dependency

##### Spark 1.6.0

```
<dependency>
    <groupId>com.ibm.ibmos2spark</groupId>
    <artifactId>ibmos2spark_2.10</artifactId>
    <version>0.0.9</version>
</dependency>
```

##### Spark 2.0.0 and greater

```
<dependency>
    <groupId>com.ibm.ibmos2spark</groupId>
    <artifactId>ibmos2spark_2.11</artifactId>
    <version>0.0.9</version>
</dependency>
```


### Snapshots

From time-to-time, a snapshot version may be released if fixes or new features are added.
The following snipets show how to install snapshot releases.
Replace the version number (`0.0.9`) in the following examples with the version you desire.

##### SBT library dependency

```
"com.ibm.ibmos2spark" %% "ibmos2spark" % "1.0.0-SNAPSHOT"
```

Add SNAPSHOT repository to build.sbt

```
resolvers +=  "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
```

##### Maven Spark 1.6.0

```
<dependency>
  <groupId>com.ibm.ibmos2spark</groupId>
  <artifactId>ibmos2spark_2.10</artifactId>
  <version>1.0.0-SNAPSHOT</version>
</dependency>
```

##### Maven Spark 2.0.0 and greater

```
<dependency>
  <groupId>com.ibm.ibmos2spark</groupId>
  <artifactId>ibmos2spark_2.11</artifactId>
  <version>1.0.0-SNAPSHOT</version>
</dependency>
```

Add SNAPSHOT repository to pom.xml

```
<repositories>
  <repository>
    <id>snapshots</id>
    <url>https://oss.sonatype.org/content/repositories/snapshots/</url>
    <releases>
      <enabled>false</enabled>
    </releases>
    <snapshots>
      <enabled>true</enabled>
    </snapshots>
  </repository>
</repositories>
```


## Usage

The instructions below demonstrate how to use this package to retrieve data from the various 
IBM Object Storage services.

These instructions will refer to the image at the top of this README.


### Cloud Object Storage 

This is the service described on the **far left** in the image above. This service is also called IBM Bluemix Cloud Object Storage (COS) in various locations. [Documentation is here](https://www.bluemix.net/docs/services/cloud-object-storage/getting-started.html).

To connect to this particular object storage offering, the `cosType` keyword argument **must be set to `bluemix_cos`**.

If you do not provide a `configurationName`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances, you will need to define separate `configurationName`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion.  

```scala
import com.ibm.ibmos2spark.CloudObjectStorage

var credentials = scala.collection.mutable.HashMap[String, String](
  "endPoint"->"xxx",
  "apiKey"->"xxx",
  "serviceId"->"xxx"
)
var bucketName = "myBucket"
var objectname = "mydata.csv"

var configurationName = "cos_config_name" // you can choose any string you want
var cos = new CloudObjectStorage(sc, credentials,
                                configurationName=configurationName,
                                cosType="bluemix_cos")
var spark = SparkSession.
    builder().
    getOrCreate()

var dfData1 = spark.
    read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").
    option("header", "true").
    option("inferSchema", "true").
    load(cos.url(bucketName, objectname))
```

##### IAM Token Authentication

Alternatively, you can connect to an IBM Bluemix COS using IAM token. Set the `authMethod` to `iam_token` and
provide the appropriate values in the credentials.

```scala
import com.ibm.ibmos2spark.CloudObjectStorage

// The credentials HashMap may be created for you with the
// "insert to code" link in your DSX notebook.

var credentials = scala.collection.mutable.HashMap[String, String](
  "endPoint"->"xxx",
  "iamToken"->"xxx",
  "serviceId"->"xxx"
)
var bucketName = "myBucket"
var objectname = "mydata.csv"

var configurationName = "cos_config_name" // you can choose any string you want
var cos = new CloudObjectStorage(sc, credentials,
                                configurationName=configurationName,
                                cosType="bluemix_cos",
                                authMethod="iam_token")
var spark = SparkSession.
    builder().
    getOrCreate()

var dfData1 = spark.
    read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").
    option("header", "true").
    option("inferSchema", "true").
    load(cos.url(bucketName, objectname))
```




### Cloud Object Storage (IaaS)

This is the service described **middle left** pane in the image above. This service is sometimes refered to 
as the Softlayer IBM Cloud Object Storage service. 
[Documentation is here](https://ibm-public-cos.github.io/crs-docs/).

If you do not provide a `configurationName`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances you will need to define separate `configurationName`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion. 


```scala
import com.ibm.ibmos2spark.CloudObjectStorage

var credentials = scala.collection.mutable.HashMap[String, String](
  "endPoint"->"https://identity.open.softlayer.com",
  "accessKey"->"xx",
  "secretKey"->"xx"
)
var bucketName = "myBucket"
var objectname = "mydata.csv"

var configurationName = "cos_config_name" // you can choose any string you want
var cos = new CloudObjectStorage(sc, credentials, configurationName=configurationName)
var spark = SparkSession.
    builder().
    getOrCreate()

var dfData1 = spark.
    read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").
    option("header", "true").
    option("inferSchema", "true").
    load(cos.url(bucketName, objectname))
```

### Object Storage OpenStack Swift (Iaas)

This is the service described in **middle right** pane in the image above (and was previously referred to 
as Softlayer Swift Object Storage).  [Documentation is here](https://ibm-public-cos.github.io/crs-docs/)

Note below that credentials are not passed in as a dictionary, like in the other implementations. 
Rather, each piece of information is supplied as a separate, required argument when instantiating
a new `softlayer` object. 


```scala
import com.ibm.ibmos2spark.softlayer

var authurl = "xx"
var tenant = "xx"
var user = "xx"
var password = "xx"

var container = "mycontainer"
var objectname = "mydata.txt"
var configurationname = "softlayerOSconnection"

var slos = new softlayer(sc, configurationname, authurl, tenant, user, password)
var rdd = sc.textFile(slos.url(container , objectname))

```

### Object Storage OpenStack Swift for Bluemix

This is the service described in **far right** pane in the image above. 
This was previously referred to as Bluemix Swift Object Storage in this documentation. It is 
referred to as ["IBM Object Storage for Bluemix" in Bluemix documenation](https://console.bluemix.net/docs/services/ObjectStorage/os_works_public.html). It has also been referred to as 
"OpenStack Swift (Cloud Foundry)". 

Credentials are passed as 
a dictionary and the `bluemix` object is used to configure the connection to 
this Object Storage service.

If you do not provide a `configurationName`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances you will need to define separate `configurationName`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion. 


```scala
import com.ibm.ibmos2spark.bluemix

// The credentials HashMap may be created for you with the
// "insert to code" link in your DSX notebook.

var credentials = scala.collection.mutable.HashMap[String, String](
  "auth_url"->"https://identity.open.softlayer.com",
  "project_id"->"xx",
  "region"->"xx",
  "user_id"->"xx",
  "password"->"xx",
)

var container = "mycontainer"
var objectname = "mydata.txt"
var configurationName = "bluemix_object_storage_connection"

var bmos = new bluemix(sc, configurationName, credentials)
var rdd = sc.textFile(bmos.url(container , objectname))

```



## Package Info

One can use the automatically generated object, `BuildInfo`, to obtain the package version
and other information. This object is automatically generated by the
[`sbt-buildinfo`](https://github.com/sbt/sbt-buildinfo) plugin.

```
import com.ibm.ibmos2spark.BuildInfo

var buildstring = BuildInfo.toString
var buildbmap = BuildInfo.toMap
var buildjson = BuildInfo.toJson
```

## Details

This library only does two things.

1. [Uses the `SparkContext.hadoopConfiguration` object to set the appropriate keys](https://github.com/SparkTC/stocator#configuration-keys) to define a connection to an object storage service.
2. Provides the caller with a URL to objects in their object store, which are typically passed to a SparkContext
object to retrieve data. 



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
