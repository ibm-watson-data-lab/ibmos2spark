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

## Apache Spark at IBM

The `stocator` and `ibmos2spark` libraries are pre-installled and available on 

* [Apache Spark through IBM Bluemix](https://console.bluemix.net/catalog/services/apache-spark)
* [IBM Analytics Engine (Beta)](https://console.bluemix.net/catalog/services/ibm-analytics-engine)  
* [IBM Data Science Experience](https://datascience.ibm.com)

## Languages

The library is implemented for use in [Python](python), [R](r) and [Scala/Java](scala). 

## Details 

This library only does two things.

1. [Uses the `SparkContext.hadoopConfiguration` object to set the appropriate keys](https://github.com/SparkTC/stocator#configuration-keys) to define a connection to an object storage service.
2. Provides the caller with a URL to objects in their object store, which are typically passed to a SparkContext
object to retrieve data. 

### Example Usage

The following code demonstrates how to use this library in Python and connect to the Cloud Object Storage 
service, described in the far left pane of the image above. 

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

configuration_name = 'my_bluemix_objectstore'  #you can give any name you like

bmos = ibmos2spark.bluemix(sc, credentials, configuration_name)  #sc is the SparkContext instance

container_name = 'some_name'
object_name = 'file_name'

data_url = bmos.url(container_name, object_name)

data = sc.textFile(data_url)
```
