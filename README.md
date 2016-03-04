# ibmos2spark

Use this when trying to access data on either a Softlayer or Bluemix ObjectStore.


### Bluemix
```python
import ibmos2spark as os2s

#To obtain these credentials in IBM Spark, click the "insert to code" 
#button below your data source found on the panel to the right of your notebook.

credentials = {
  'auth_url': 'https://identity.open.softlayer.com',  #your URL might be different
  'project_id': 'sssssssss',
  'region': 'dallas',
  'user_id': 'uuuuuuuuuuu',
  'username': 'uuuuuuuuuuu',
  'password': 'ppppppppppp',
}

credentials['name'] = 'my_bluemix_os'  #you can give any name you like

bmos = os2s.bluemix(sc, credentials)  #sc is the SparkContext instance

data = sc.textFile(bmos.url(container_name, file_name))
```


### Softlayer
```python
import ibmos2spark as os2s

#you need to know the credentials to your Softlayer ObjectStore.

#sc is the SparkContext instance
#you can give any name you like

slos = os2s.softlayer(sc, "my_softlayer_os", auth_url, username, password)

data = sc.textFile(slos.url(container_name, file_name))
```

