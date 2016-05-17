# Copyright (c) 2016 IBM. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License a
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Constructs an object to configure the connection to the ObjectStores
and generate the swifturl.

"""
  
def swifturl(name, container_name, object_name):
  return 'swift://{}.{}/{}'.format(container_name, name, object_name)

def swifturl2d(name, container_name, object_name):
  return 'swift2d://{}.{}/{}'.format(container_name, name, object_name)

class softlayer(object):

  def __init__(self, sparkcontext, name, auth_url, username, password):
    '''
    sparkcontext is a SparkContext object.
    name is a string that can be anything other than an empty string.
    auth_url, username and password are string credentials for your
    Softlayer Objectstore

    '''
    self.name = name

    prefix = "fs.swift.service." + name 
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set(prefix + ".auth.url", auth_url)
    hconf.set(prefix + ".username", username)
    hconf.set(prefix + ".tenant", username)
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".apikey", password)
    hconf.setBoolean(prefix + ".public", True) 
    hconf.set(prefix + ".use.get.auth", "true")
    hconf.setBoolean(prefix + ".location-aware", False)
    hconf.set(prefix + ".password", password)

  def url(self, container_name, object_name):
    return swifturl(self.name, container_name, object_name)

class softlayer2d(object):

  def __init__(self, sparkcontext, name, auth_url, tenant, username, password, 
    swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'):
    '''
    sparkcontext is a SparkContext object.
    name is a string that can be anything other than an empty string.
    auth_url, username and password are string credentials for your
    Softlayer Objectstore

    '''
    self.name = name

    prefix = "fs.swift2d.service." + name 
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set("fs.swift2d.impl", swift2d_driver)
    hconf.set(prefix + ".auth.url", auth_url)
    hconf.set(prefix + ".username", username)
    hconf.set(prefix + ".tenant", tenant)
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".auth.method", "swiftauth")
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".apikey", password)
    hconf.setBoolean(prefix + ".public", True) 
    hconf.set(prefix + ".use.get.auth", "true")
    hconf.setBoolean(prefix + ".location-aware", False)
    hconf.set(prefix + ".password", password)

  def url(self, container_name, object_name):
    return swifturl2d(self.name, container_name, object_name)

class bluemix(object):

  def __init__(self, sparkcontext, credentials):
    '''
    sparkcontext is a SparkContext object.

    credentials is a dictionary with the following required keys:
      
      auth_url
      project_id
      user_id
      password
      region
      name #can be any string you choose

    When using this from a IBM Spark service instance that
    is configured to connect to particular Bluemix object store
    instances, the values for these credentials can be obtained 
    by clicking on the 'insert to code' link just below a data
    source. 
    '''
    self.name = credentials['name']

    prefix = "fs.swift.service." + credentials['name'] 
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set(prefix + ".auth.url", credentials['auth_url']+'/v3/auth/tokens')
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".auth.method","keystoneV3 ")
    hconf.set(prefix + ".tenant", credentials['project_id'])
    hconf.set(prefix + ".username", credentials['user_id'])
    hconf.set(prefix + ".password", credentials['password'])
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".region", credentials['region'])
    hconf.setBoolean(prefix + ".public", True)

  def url(self, container_name, object_name):
    return swifturl(self.name, container_name, object_name)

class bluemix2d(object):

  def __init__(self, sparkcontext, credentials,
    swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'):
    '''
    sparkcontext is a SparkContext object.

    credentials is a dictionary with the following required keys:
      
      auth_url
      project_id
      user_id
      password
      region
      name #can be any string you choose

    When using this from a IBM Spark service instance that
    is configured to connect to particular Bluemix object store
    instances, the values for these credentials can be obtained 
    by clicking on the 'insert to code' link just below a data
    source. 
    '''
    self.name = credentials['name']


    prefix = "fs.swift2d.service." + credentials['name'] 
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set("fs.swift2d.impl", swift2d_driver)
    hconf.set(prefix + ".auth.url", credentials['auth_url']+'/v3/auth/tokens')
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".auth.method","keystoneV3 ")
    hconf.set(prefix + ".tenant", credentials['project_id'])
    hconf.set(prefix + ".username", credentials['user_id'])
    hconf.set(prefix + ".password", credentials['password'])
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".region", credentials['region'])
    hconf.setBoolean(prefix + ".public", True)

  def url(self, container_name, object_name):
    return swifturl2d(self.name, container_name, object_name)
