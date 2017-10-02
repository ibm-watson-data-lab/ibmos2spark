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

This library is now installed by default on IBM Apache Spark.

```
pip install --user --upgrade ibmos2spark
```

## Usage

The usage of this package depends on *from where* your Object Storage instance was created. This package
is intended to connect to IBM's Object Storage instances (Swift OS). This OS can be obtained from Bluemix or Data Science Experience (DSX) or from a separate account on IBM Softlayer. The package also supports IBM Cloud Object Storage as well (COS).
The instructions below show how to connect to either type of instance.

The connection setup is essentially the same. But the difference for you is how you deliver the
credentials. If your Object Storage was created with Bluemix/DSX, with a few clicks on the side-tab
within a DSX Jupyter notebook, you can obtain your account credentials in the form of a Python dictionary.
If your Object Storage was created with a Softlayer account, each part of the credentials will
be found as text that you can copy and paste into the example code below.

### Softlayer CloudObjectStorage / Data Science Experience
```python
import ibmos2spark

credentials = {
  'endpoint': 'https://s3-api.objectstorage.softlayer.net/',  #just an example. Your url might be different
  'access_key': '',
  'secret_key': ''
}

configuration_name = 'cos_config_string'  #you can give any string you like
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name)  #sc is the SparkContext instance.

bucket_name = 'some_bucket_name'
object_name = 'file1'
data = sc.textFile(cos.url(object_name, bucket_name))
```

### Bluemix CloudObjectStorage / Data Science Experience
The class CloudObjectStorage allows you to connect to bluemix cos. You can connect to bluemix using api keys
as follows:

```pythonw
import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'XXX',
    'api_key': 'XXX',
    'service_id': 'XXX'
}

configuration_name = 'os_bluemix_cos_config'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos')

bucket_name = 'bucket_name'
object_name = 'file_name'
data = sc.textFile(cos.url(object_name, bucket_name))
```

Alternatively, you can connect to bluemix cos using IAM token. Example:
```pythonw
import ibmos2spark

# @hidden_cell
credentials = {
    'endpoint': 'XXX',
    'iam_token': 'eyJraWQXXXX .... X',
    'service_id': 'XXX'
}

configuration_name = 'os_bluemix_cos_config'
cos = ibmos2spark.CloudObjectStorage(sc, credentials, configuration_name, 'bluemix_cos', 'iam_token')

bucket_name = 'bucket_name'
object_name = 'file_name'
data = sc.textFile(cos.url(object_name, bucket_name))
```


### Bluemix Swift Object Storage / Data Science Experience

```python
import ibmos2spark

#To obtain these credentials in IBM Spark, click the "insert to code"
#button below your data source found on the panel to the right of your notebook.

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


### Softlayer Swift Object Storage


```python
import ibmos2spark

#you need to know the credentials to your Softlayer ObjectStore.
auth_url = ''
tenant = ''
username = ''
password = ''

#you can give any name you like
configuration_name = "my_softlayer_os"

#sc is the SparkContext instance
slos = ibmos2spark.softlayer(sc, configuration_name, auth_url, tenant, username, password)

data = sc.textFile(slos.url(container_name, object_name))
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
