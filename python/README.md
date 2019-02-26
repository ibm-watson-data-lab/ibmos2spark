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

This library is published on PyPI and may be installed with `pip`.

```
pip install ibmos2spark
```

## Apache Spark at IBM

The `stocator` and `ibmos2spark` libraries are pre-installled and available on 

* [Apache Spark through IBM Bluemix](https://console.bluemix.net/catalog/services/apache-spark)
* [IBM Analytics Engine (Beta)](https://console.bluemix.net/catalog/services/ibm-analytics-engine)  
* [IBM Data Science Experience](https://datascience.ibm.com)



## Usage

The instructions below demonstrate how to use this package to retrieve data from the various 
IBM Object Storage services.

These instructions will refer to the image at the top of this README.


### Cloud Object Storage 

This is the service described on the **far left** in the image above. This service is also called IBM Bluemix Cloud Object Storage (COS) in various locations. [Documentation is here](https://www.bluemix.net/docs/services/cloud-object-storage/getting-started.html).

To connect to this particular object storage offering, the `cos_type` keyword argument **must be set to `bluemix_cos`**.

If you do not provide a `configuration_name`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances, you will need to define separate `configuration_name`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion.  

```python
import ibmos2spark

credentials = {
    'endpoint': 'XXX',
    'api_key': 'XXX',
    'service_id': 'XXX'
}

# This name could be arbitrary
configuration_name = 'os_bluemix_cos_config'

cos = ibmos2spark.CloudObjectStorage(sc, credentials,
                                    configuration_name=configuration_name,
                                    cos_type='bluemix_cos')

# The `sc` object is your SparkContext object
# The `cos` object will provide the URL for SparkContext to retrieve your data
# NOTE the counter-intuitive order of 'object_name' followed by 'bucket_name' here

bucket_name = 'bucket_name'
object_name = 'file_name'
data_url = cos.url(object_name, bucket_name)

data = sc.textFile(data_url)
```

##### IAM Token Authentication

Alternatively, you can connect to an IBM Bluemix COS using IAM token. Set the `auth_method` to `api_key` and
provide the appropriate values in the credentials.


```python
import ibmos2spark

credentials = {
    'endpoint': 'XXX',
    'api_key': 'eyJraWQXXXX .... X',
    'service_id': 'crn:v1:bluemix:public:cloud-object-storage:global:a/XXX'
}

# This name could be arbitrary
configuration_name = 'os_bluemix_cos_config'
cos = ibmos2spark.CloudObjectStorage(sc, credentials,
                                      configuration_name=configuration_name,
                                      cos_type='bluemix_cos',
                                      auth_method='api_key')

# The `sc` object is your SparkContext object
# The `cos` object will provide the URL for SparkContext to retrieve your data
# NOTE the counter-intuitive order of 'object_name' followed by 'bucket_name' here

bucket_name = 'bucket_name'
object_name = 'file_name'
data_url = cos.url(object_name, bucket_name)

data = sc.textFile(data_url)
```


### Cloud Object Storage (IaaS)

This is the service described **middle left** pane in the image above. This service is sometimes refered to 
as the Softlayer IBM Cloud Object Storage service. 
[Documentation is here](https://ibm-public-cos.github.io/crs-docs/).

If you do not provide a `configuration_name`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances you will need to define separate `configuration_name`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion. 

```python
import ibmos2spark

credentials = {
  'endpoint': 'https://s3-api.objectstorage.softlayer.net/',  #just an example. Your url might be different
  'access_key': '',
  'secret_key': ''
}

configuration_name = 'cos_config_string'  #you can give any string you like
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name=configuration_name)  #sc is the SparkContext instance.

# The `sc` object is your SparkContext object
# The `cos` object will provide the URL for SparkContext to retrieve your data
# NOTE the counter-intuitive order of 'object_name' followed by 'bucket_name' here

bucket_name = 'bucket_name'
object_name = 'file_name'
data_url = cos.url(object_name, bucket_name)

data = sc.textFile(data_url)

```



### Object Storage OpenStack Swift (Iaas)

This is the service described in **middle right** pane in the image above (and was previously referred to 
as Softlayer Swift Object Storage).  [Documentation is here](https://ibm-public-cos.github.io/crs-docs/)

Note below that credentials are not passed in as a dictionary, like in the other implementations. 
Rather, each piece of information is supplied as a separate, required argument when instantiating
a new `softlayer` object. 


```python
import ibmos2spark

#you need to know the credentials to your Softlayer ObjectStore.
auth_url = ''
tenant = ''
username = ''
password = ''

#you can give any name you like. This is required. 
configuration_name = "my_softlayer_os"

#sc is the SparkContext instance
slos = ibmos2spark.softlayer(sc, configuration_name, auth_url, tenant, username, password)

data = sc.textFile(slos.url(container_name, object_name))
```

### Object Storage OpenStack Swift for Bluemix

This is the service described in **far right** pane in the image above. 
This was previously referred to as Bluemix Swift Object Storage in this documentation. It is 
referred to as ["IBM Object Storage for Bluemix" in Bluemix documenation](https://console.bluemix.net/docs/services/ObjectStorage/os_works_public.html). It has also been referred to as 
"OpenStack Swift (Cloud Foundry)". 

Credentials are passed as 
a dictionary and the `bluemix` object is used to configure the connection to 
this Object Storage service.

If you do not provide a `configuration_name`, 
a default value will be used (`service`). However, if you are reading or 
writing to multiple Object Storage instances you will need to define separate `configuration_name`
values for each Object Storage instance. Otherwise, only one connection will be 
configured at a time, potentially causing errors and confusion. 

```python
import ibmos2spark

credentials = {
  'auth_url': 'https://identity.open.softlayer.com',  #your URL might be different
  'project_id': '',
  'region': '',
  'user_id': '',
  'username': '',
  'password': '',
}

configuration_name = 'my_bluemix_os'  #you can give any name you like

bmos = ibmos2spark.bluemix(sc, credentials, configuration_name)  #sc is the SparkContext instance

data = sc.textFile(bmos.url(container_name, object_name))
```


## Details

This library only does two things.

1. [Uses the `SparkContext.hadoopConfiguration` object to set the appropriate keys](https://github.com/SparkTC/stocator#configuration-keys) to define a connection to an object storage service.
2. Provides the caller with a URL to objects in their object store, which are typically passed to a SparkContext
object to retrieve data. 



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
