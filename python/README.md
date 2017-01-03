# ibmos2spark

The package configures Spark Hadoop configurations for connecting to 
Softlayer and IBM Bluemix Object Stores with the 'swift' or 'swift2d' protocol. 

It is recommended to use 'swift2d' instead of the previous version. 
The new version allows for more flexible names (underscores) and is faster.

### Bluemix

#### Using Swift (version 1) Driver
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

#you can give any name as long as it does NOT contain an underscore
configuration_name = 'myBluemixOs'  

bmos = ibmos2spark.bluemix(sc, credentials, configuration_name)  #sc is the SparkContext instance

#note, the container name also cannot contain an underscore. If your container name
#includes an underscore, use the swift2d driver instead. 
data = sc.textFile(bmos.url(container_name, object_name))
```

#### Using Swift2d Driver

The useage is exactly the same as above except that you use a different object.  
In this case `bluemix2d`.

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

bmos = ibmos2spark.bluemix2d(sc, credentials, configuration_name)  #sc is the SparkContext instance

data = sc.textFile(bmos.url(container_name, object_name))
```


### Softlayer

#### Using Swift Driver

```python
import ibmos2spark

#you need to know the credentials to your Softlayer ObjectStore.
auth_url = ''
username = ''
password = ''

#you can give any name as long as it does NOT contain an underscore
configuration_name = "mySoftlayerOs"

#sc is the SparkContext instance
slos = ibmos2spark.softlayer(sc, configuration_name, auth_url, username, password)

#note, the container name also cannot contain an underscore. If your container name
#includes an underscore, use the swift2d driver instead. 
data = sc.textFile(slos.url(container_name, object_name))
```

#### Using Swift2d Driver

The useage is exactly the same as above except that you use a different object.  
In this case `softlayer2d`.

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
slos = ibmos2spark.softlayer2d(sc, configuration_name, auth_url, tenant, username, password)

data = sc.textFile(slos.url(container_name, object_name))
```


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
