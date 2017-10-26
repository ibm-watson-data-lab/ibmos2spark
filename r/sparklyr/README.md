# ibmos2sparklyr

The `ibmos2park` library facilitates data read/write connections between Apache Spark clusters and the various 
[IBM Object Storage services](https://console.bluemix.net/catalog/infrastructure/object-storage-group). 

![IBM Object Storage Services](fig/ibm_objectstores.png "IBM Object Storage Services")

### Object Storage Documentation

* [Cloud Object Storage](https://www.bluemix.net/docs/services/cloud-object-storage/getting-started.html) **Not Yet Supported.**
* [Cloud Object Storage (IaaS)](https://ibm-public-cos.github.io/crs-docs/) **Not Yet Supported.**
* [Object Storage OpenStack Swift (IaaS)](https://ibm-public-cos.github.io/crs-docs/)
* [Object Storage OpenStack Swift for Bluemix](https://www.ng.bluemix.net/docs/services/ObjectStorage/index.html)



## Requirements

* Apache Spark with `stocator` library

The easiest way to install the `stocator` library with Apache Spark is to 
[pass the Maven coordinates at launch](https://spark-packages.org/package/SparkTC/stocator).
Other installation options are described in the [`stocator` documentation](https://github.com/SparkTC/stocator).


## Apache Spark at IBM

The `stocator` library is pre-installled and available on 

* [Apache Spark through IBM Bluemix](https://console.bluemix.net/catalog/services/apache-spark)
* [IBM Analytics Engine (Beta)](https://console.bluemix.net/catalog/services/ibm-analytics-engine)  
* [IBM Data Science Experience](https://datascience.ibm.com)

## Installation 

    library(devtools)
    devtools::install_url("https://github.com/ibm-cds-labs/ibmos2spark/archive/<version>.zip", subdir= "r/sparklyr/",dependencies = FALSE)

where `version` should be a tagged release, such as `1.0.2`. 


###### WARNING

In IBM Data Science Experience, please be sure to include the `dependencies = FALSE` flag when 
calling `devtools::install_url`. If you forget to do this, you will most likely overwrite DSX's 
special flavor of sparklyr, which will break your connection to IBM Spark Services. To repair this,
go into your local R repo store ("/home/rstudio/R/x86_64-redhat-linux-gnu-library/RVERSION/") 
where RVERSION is the newest install of R (currently 3.3) and delete the `sparklyr` folder. 
After deleting, choose File->Quit Session to refresh your R kernel. These steps will refresh your 
sparklyr package to the special DSX version. 


## Usage

The instructions below demonstrate how to use this package to retrieve data from the various 
IBM Object Storage services.

These instructions will refer to the image at the top of this README.

### Cloud Object Storage 

This is the service described on the **far left** in the image above. This service is also called IBM Bluemix Cloud Object Storage (COS) in various locations. [Documentation is here](https://www.bluemix.net/docs/services/cloud-object-storage/getting-started.html).

Not Yet Implemented.

### Cloud Object Storage (IaaS)

This is the service described **middle left** pane in the image above. This service is sometimes refered to 
as the Softlayer IBM Cloud Object Storage service. 
[Documentation is here](https://ibm-public-cos.github.io/crs-docs/).

Not Yet Implemented.

### Object Storage OpenStack Swift (Iaas)

This is the service described in **middle right** pane in the image above (and was previously referred to 
as Softlayer Swift Object Storage).  [Documentation is here](https://ibm-public-cos.github.io/crs-docs/)

Note below that credentials are not passed in as a list of key-value pairs, like in the other implementations. 
Rather, each piece of information is supplied as a separate, required argument when instantiating
a new `softlayer` object. 

```
library(ibmos2sparklyr)
configurationname = "softlayerOScon" #can be any any name you like (allows for multiple configurations)

slconfig = softlayer(sparkcontext=sc, 
             name=configurationname, 
             auth_url="https://identity.open.softlayer.com",
             tenant = "XXXXX", 
             username="XXXXX", 
             password="XXXXX"
       )
       
container = "my_container" # name of your object store container
object = "my_data.csv" # name of object that you want to retrieve in the container
spark_object_name = "dataFromSwift" # name to assign to the new spark object

data = sparklyr::spark_read_csv(sc, spark_object_name,slconfig$url(container,object))
```

### Object Storage OpenStack Swift for Bluemix

This is the service described in **far right** pane in the image above. 
This was previously referred to as Bluemix Swift Object Storage in this documentation. It is 
referred to as ["IBM Object Storage for Bluemix" in Bluemix documenation](https://console.bluemix.net/docs/services/ObjectStorage/os_works_public.html). It has also been referred to as 
"OpenStack Swift (Cloud Foundry)". 

Credentials are passed as 
a list of key-value pairs and the `bluemix` object is used to configure the connection to 
this Object Storage service.

If you do not provide a `configurationName`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances you will need to define separate `configurationName`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion. 

```
library(ibmos2sparklyr)
configurationname = "bluemixOScon" #can be any any name you like (allows for multiple configurations)

# In DSX notebooks, the "insert to code" will insert this credentials list for you
creds = list(
        auth_url="https://identity.open.softlayer.com",
        region="dallas", 
        project_id = "XXXXX", 
        user_id="XXXXX", 
        password="XXXXX")
        
bmconfig = bluemix(sparkcontext=sc, name=configurationname, credentials = creds)
       
container = "my_container" # name of your object store container
object = "my_data.csv" # name of object that you want to retrieve in the container
spark_object_name = "dataFromSwift" # name to assign to the new spark object

data = sparklyr::spark_read_csv(sc, spark_object_name,bmconfig$url(container,object))
```




## License 

Copyright 2017 IBM Cloud Data Services

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
