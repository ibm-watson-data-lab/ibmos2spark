# ibmos2spark

The package sets Spark Hadoop configurations for connecting to 
IBM Bluemix Object Storage and Softlayer Account Object Storage instances
with the swift protocol. This packages uses the new [swift2d/stocator](https://github.com/SparkTC/stocator) protocol, availble
on the latest IBM Spark Service instances (and through IBM Data Science Experience). 

## Installation

```
pip install --user --upgrade ibmos2spark
```

## Usage

### Bluemix

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


### Softlayer


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
