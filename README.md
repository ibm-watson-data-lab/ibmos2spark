# ibmos2spark

Use this when trying to access data on either a Softlayer or Bluemix ObjectStore.


### Bluemix

#### Using Swift Driver
```python
import ibmos2spark as oss

#To obtain these credentials in IBM Spark, click the "insert to code" 
#button below your data source found on the panel to the right of your notebook.

credentials = {
  'auth_url': 'https://identity.open.softlayer.com',  #your URL might be different
  'project_id': '',
  'region': 'dallas',
  'user_id': '',
  'username': '',
  'password': '',
}

configuration_name = 'my_bluemix_os'  #you can give any name you like

bmos = oss.bluemix(sc, credentials, configuration_name)  #sc is the SparkContext instance

data = sc.textFile(bmos.url(container_name, file_name))
```

#### Using Stocator (Swift2d) Driver

The use case is exactly the same as above except that you use a different object.  
In this case `bluemix2d`.

```python
import ibmos2spark as oss

#To obtain these credentials in IBM Spark, click the "insert to code" 
#button below your data source found on the panel to the right of your notebook.

credentials = {
  'auth_url': 'https://identity.open.softlayer.com',  #your URL might be different
  'project_id': '',
  'region': 'dallas',
  'user_id': '',
  'username': '',
  'password': '',
}

configuration_name = 'my_bluemix_os'  #you can give any name you like

bmos = oss.bluemix2d(sc, credentials)  #sc is the SparkContext instance

data = sc.textFile(bmos.url(container_name, file_name))
```


### Softlayer

#### Using Swift Driver

```python
import ibmos2spark as oss

#you need to know the credentials to your Softlayer ObjectStore.

#sc is the SparkContext instance
#you can give any name you like

slos = oss.softlayer(sc, "my_softlayer_os", auth_url, username, password)

data = sc.textFile(slos.url(container_name, file_name))
```

#### Using Stocator (Swift2d) Driver

The use case is exactly the same as above except that you use a different object.  
In this case `softlayer2d`.

```python
import ibmos2spark as oss

#you need to know the credentials to your Softlayer ObjectStore.

#sc is the SparkContext instance
#you can give any name you like

slos = oss.softlayer2d(sc, "my_softlayer_os", auth_url, tenant, username, password)

data = sc.textFile(slos.url(container_name, file_name))
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
