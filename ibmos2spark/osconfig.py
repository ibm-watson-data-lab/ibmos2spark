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
  
import warnings

def swifturl(name, container_name, object_name):
  return 'swift://{}.{}/{}'.format(container_name, name, object_name)

def swifturl2d(name, container_name, object_name):
  return 'swift2d://{}.{}/{}'.format(container_name, name, object_name)

class softlayer(object):

  def __init__(self, sparkcontext, name, auth_url, username, password, 
                public=False):
    '''
    sparkcontext is a SparkContext object.

    name is a string that identifies this configuration. You can
        use any string you like. This allows you to create
        multiple configurations to different Object Storage accounts.

    auth_url, username and password are string credentials for your
    Softlayer Object Store
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
    hconf.setBoolean(prefix + ".public", public) 
    hconf.set(prefix + ".use.get.auth", "true")
    hconf.setBoolean(prefix + ".location-aware", False)
    hconf.set(prefix + ".password", password)

  def url(self, container_name, object_name):
    return swifturl(self.name, container_name, object_name)

class softlayer2d(object):

  def __init__(self, sparkcontext, name, auth_url, tenant, username, password, 
    swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem', public=False):
    '''
    sparkcontext is a SparkContext object.

    name is a string that identifies this configuration. You can
        use any string you like. This allows you to create
        multiple configurations to different Object Storage accounts.

    auth_url, username and password are string credentials for your
    Softlayer Object Store
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
    hconf.setBoolean(prefix + ".public", public) 
    hconf.set(prefix + ".use.get.auth", "true")
    hconf.setBoolean(prefix + ".location-aware", False)
    hconf.set(prefix + ".password", password)

  def url(self, container_name, object_name):
    return swifturl2d(self.name, container_name, object_name)

class bluemix(object):

  def __init__(self, sparkcontext, credentials, name=None, public=False):
    '''
    sparkcontext:  a SparkContext object.

    credentials:  a dictionary with the following required keys:
      
      auth_url
      project_id (or projectId)
      user_id (or userId)
      password
      region

    and optional key:
      name  #[to be deprecated] The name of the configuration.

    name:  string that identifies this configuration. You can
        use any string you like. This allows you to create
        multiple configurations to different Object Storage accounts.
        This is not required at the moment, since credentials['name']
        is still supported.

    When using this from a IBM Spark service instance that
    is configured to connect to particular Bluemix object store
    instances, the values for these credentials can be obtained
    by clicking on the 'insert to code' link just below a data
    source.
    '''

    if name:
        self.name = name
    else:
        self.name = credentials['name']
        warnings.warn('credentials["name"] key will be deprecated. Use the "name" argument in object contructor', DeprecationWarning)

    try:
        user_id = credentials['user_id']
    except KeyError as e:
        user_id = credentials['userId'] 

    try:
        tenant = credentials['project_id']
    except KeyError as e:
        tenant = credentials['projectId'] 

    prefix = "fs.swift.service." + self.name
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set(prefix + ".auth.url", credentials['auth_url']+'/v3/auth/tokens')
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".auth.method","keystoneV3 ")
    hconf.set(prefix + ".tenant", tenant)
    hconf.set(prefix + ".username", user_id)
    hconf.set(prefix + ".password", credentials['password'])
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".region", credentials['region'])
    hconf.setBoolean(prefix + ".public", False)

  def url(self, container_name, object_name):
    return swifturl(self.name, container_name, object_name)

class bluemix2d(object):

  def __init__(self, sparkcontext, credentials, name=None,
    swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem', 
    public=False):
    '''
    sparkcontext:  a SparkContext object.

    credentials:  a dictionary with the following required keys:
      
      auth_url
      project_id (or projectId)
      user_id (or userId)
      password
      region

    and optional key:
      name  #[to be deprecated] The name of the configuration.

    name:  string that identifies this configuration. You can
        use any string you like. This allows you to create
        multiple configurations to different Object Storage accounts.
        This is not required at the moment, since credentials['name']
        is still supported.

    When using this from a IBM Spark service instance that
    is configured to connect to particular Bluemix object store
    instances, the values for these credentials can be obtained
    by clicking on the 'insert to code' link just below a data
    source.

    '''

    if name:
        self.name = name
    else:
        self.name = credentials['name']
        warnings.warn('credentials["name"] key will be deprecated. Use the "name" argument in object contructor', DeprecationWarning)


    try:
        user_id = credentials['user_id']
    except KeyError as e:
        user_id = credentials['userId'] 

    try:
        tenant = credentials['project_id']
    except KeyError as e:
        tenant = credentials['projectId'] 

    prefix = "fs.swift2d.service." + self.name
    hconf = sparkcontext._jsc.hadoopConfiguration()
    hconf.set("fs.swift2d.impl", swift2d_driver)
    hconf.set(prefix + ".auth.url", credentials['auth_url']+'/v3/auth/tokens')
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".auth.method","keystoneV3 ")
    hconf.set(prefix + ".tenant", tenant)
    hconf.set(prefix + ".username", user_id)
    hconf.set(prefix + ".password", credentials['password'])
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".region", credentials['region'])
    hconf.setBoolean(prefix + ".public", public)

  def url(self, container_name, object_name):
    return swifturl2d(self.name, container_name, object_name)
