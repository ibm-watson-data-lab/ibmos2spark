# ibmos2spark

The package sets Spark Hadoop configurations for connecting to 
Softlayer and IBM Bluemix Object Stores with the swift protocol. This packages
uses the new 'swift2d' protocol. 


## Build

This builds jar files for both Spark 1.6.0 (Scala 2.10.4) and Spark 2.0.2 (Scala 2.11.8)

```
sbt +assembly
```

## Installation

We are in the process of publishing these `jar` files to a Maven repo. For now, the `%AddJar` magic funtion within 
a Scala notebook will install the package.

### Spark 1.6.0

```scala
%AddJar https://github.com/gadamc/jartest/raw/master/scala/jars/scala-2.10/ibmos2spark-assembly-0.0.7dev.jar -f 
```


### Spark 2.0.2

```scala
%AddJar https://github.com/gadamc/jartest/raw/master/scala/jars/scala-2.11/ibmos2spark-assembly-0.0.7dev.jar -f
```


## Usage

### Bluemix


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
var rdd = sc.textFile(bmos.url( container , objectname))

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
var rdd = sc.textFile(slos.url( container , objectname))

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
