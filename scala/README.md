# ibmos2spark

The package sets Spark Hadoop configurations for connecting to
IBM Bluemix Object Storage and Softlayer Account Object Storage instances. This packages uses the new [stocator](https://github.com/SparkTC/stocator) driver, which implements the `swift2d` protocol, and is availble
on the latest IBM Apache Spark Service instances (and through IBM Data Science Experience).

Using the `stocator` driver connects your Spark executor nodes directly
to your data in object storage.
This is an optimized, high-performance method to connect Spark to your data. All IBM Apache Spark kernels
are instantiated with the `stocator` driver in the Spark kernel's classpath.
You can also run this locally by installing the [stocator driver](https://github.com/SparkTC/stocator)
and adding it to your local Apache Spark kernel's classpath.


## Installation

This library is cross-built on both Scala 2.10 (for Spark 1.6.0) and Scala 2.11 (for Spark 2.0.0 and greater)

### Releases

#### SBT library dependency

```
"com.ibm.ibmos2spark" %% "ibmos2spark" % "0.0.8"
```

#### Maven Dependency

##### Spark 1.6.0

```
<dependency>
    <groupId>com.ibm.ibmos2spark</groupId>
    <artifactId>ibmos2spark_2.10</artifactId>
    <version>0.0.8</version>
</dependency>
```

##### Spark 2.0.0 and greater

```
<dependency>
    <groupId>com.ibm.ibmos2spark</groupId>
    <artifactId>ibmos2spark_2.11</artifactId>
    <version>0.0.8</version>
</dependency>
```


#### IBM Spark Service  

The `ibmos2spark` Scala library package is now pre-installed on IBM Apache Spark as a service. This includes
service instances created in Bluemix or in Data Science Experience.

### Snapshots

From time-to-time, a snapshot version may be released if fixes or new features are added.
The following snipets show how to install snapshot releases.
Replace the version number (`0.0.8`) in the following examples with the version you desire.

##### SBT library dependency

```
"com.ibm.ibmos2spark" %% "ibmos2spark" % "0.0.9-SNAPSHOT"
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
  <version>0.0.9-SNAPSHOT</version>
</dependency>
```

##### Maven Spark 2.0.0 and greater

```
<dependency>
  <groupId>com.ibm.ibmos2spark</groupId>
  <artifactId>ibmos2spark_2.11</artifactId>
  <version>0.0.9-SNAPSHOT</version>
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


##### IBM Data Science Experience Spark 1.6.0 (Scala 2.10)

```scala
%AddJar https://oss.sonatype.org/content/repositories/snapshots/com/ibm/ibmos2spark/ibmos2spark_2.10/0.0.9-SNAPSHOT/ibmos2spark_2.10-0.0.9-SNAPSHOT.jar -f
```

##### IBM Data Science Experience Spark 2.0.2 (Scala 2.11)

```scala
%AddDeps com.ibm.ibmos2spark ibmos2spark_2.11 0.0.9-SNAPSHOT --repository https://oss.sonatype.org/content/repositories/snapshots/
```

## Usage

The usage of this package depends on *from where* your Object Storage instance was created. This package
is intended to connect to IBM's Object Storage instances obtained from Bluemix or Data Science Experience
(DSX) or from a separate account on IBM Softlayer. It also supports IBM cloud object storage (COS).
The instructions below show how to connect to either type of instance.

The connection setup is essentially the same. But the difference for you is how you deliver the
credentials. If your Object Storage was created with Bluemix/DSX, with a few clicks on the side-tab
within a DSX Jupyter notebook, you can obtain your account credentials in the form of a HashMap object.
If your Object Storage was created with a Softlayer account, each part of the credentials will
be found as text that you can copy and paste into the example code below.

### IBM Cloud Object Storage / Data Science Experience
```scala
import com.ibm.ibmos2spark.CloudObjectStorage

// The credentials HashMap may be created for you with the
// "insert to code" link in your DSX notebook.

var credentials = scala.collection.mutable.HashMap[String, String](
  "endPoint"->"https://identity.open.softlayer.com",
  "accessKey"->"xx",
  "secretKey"->"xx"
)
var bucketName = "myBucket"
var objectname = "mydata.csv"

var configurationName = "cos_config_name" // you can choose any string you want
var cos = new CloudObjectStorage(sc, credentials, configurationName)
var spark = SparkSession.
    builder().
    getOrCreate()

var dfData1 = spark.
    read.format("org.apache.spark.sql.execution.datasources.csv.CSVFileFormat").
    option("header", "true").
    option("inferSchema", "true").
    load(cos.url(bucketName, objectname))
```


### Bluemix / Data Science Experience


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
var objectname = "mydata"
var configurationname = "bluemix_object_storage_connection"

var bmos = new bluemix(sc, configurationname, credentials)
var rdd = sc.textFile(bmos.url(container , objectname))

```


### Softlayer



```scala
import com.ibm.ibmos2spark.softlayer

var authurl = "xx"
var tenant = "xx"
var user = "xx"
var password = "xx"

var container = "mycontainer"
var objectname = "mydata"
var configurationname = "softlayerOSconnection"

var slos = new softlayer(sc, configurationname, authurl, tenant, user, password)
var rdd = sc.textFile(slos.url(container , objectname))

```

### Package Info

One can use the automatically generated object, `BuildInfo`, to obtain the package version
and other information. This object is automatically generated by the
[`sbt-buildinfo`](https://github.com/sbt/sbt-buildinfo) plugin.

```
import com.ibm.ibmos2spark.BuildInfo

var buildstring = BuildInfo.toString
var buildbmap = BuildInfo.toMap
var buildjson = BuildInfo.toJson
```

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
