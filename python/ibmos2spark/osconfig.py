# Copyright (c) 2017 IBM. All rights reserved.
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

def swifturl2d(name, container_name, object_name):
  return 'swift2d://{}.{}/{}'.format(container_name, name, object_name)

class softlayer(object):

  def __init__(self, sparkcontext, name, auth_url, tenant, username, password=None, public=False,
    swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'):
    '''
    sparkcontext is a SparkContext object.

    name is a string that identifies this configuration. You can
        use any string you like. This allows you to create
        multiple configurations to different Object Storage accounts.

    auth_url, tenant, username and password are string credentials for your
    Softlayer Object Store

    Example: 

      slos = softlayer(sc, 'mySLOS', 'https://dal05.objectstorage.softlayer.net/auth/v1.0',
                       'IBMOS278685-10','username@somewhere.com', 'password_234234ada')


    CLASS UPDATE INFOMATION:

    The older 'swift' protocol for Softlayer Object Storage accounts no
    longer properly works in IBM Spark service instances. Code that used
    this class should have failed when attempted to access data with swift.

    As of the version 0.0.7 update, support for the old protocol has been removed in
    favor of the new swift2d/stocator protocol. 

    Subsequently, the __init__ for this class has been changed!  

    However, to support older code that may have been unused since this transition, 
    this __init__ function will check the arguments and attempt to determine
    the proper credentials. Specifically, if the <password> is None, then
    the <tenant> argument will be interpreted as <tenant>:<username> and the 
    <username> argument will be interpreted as the <password> value. This is because
    the <username> for Softlayer keystone 1 authentication is equivalent to <tenant>:<username>. 
    For example, typcial usernames look like 'IBMOS278685-10:<email>', as shown here
    http://knowledgelayer.softlayer.com/procedure/how-do-i-access-object-storage-command-line. 
 

    Therefore, this class will attempt to extract tenant, username and password from
    uses such as

      slos = softlayer(sc, 'mySLOS', 'https://dal05.objectstorage.softlayer.net/auth/v1.0',
                       'IBMOS278685-10:username@somewhere.com', 'password_234234ada')

    by splitting 'IBMOS278685-10:username@somewhere.com'. In this example call, password=None
    because only 5 arguments were passed in.

    '''
    if password is None:
      msg = '''
               password was set to None! 
               Attempting to interpret tentant = tenant:username and username=password.
               This is an attempt to support older code that may have missed the transition or
               errors using the old swift protocol connection to Softlayer Object Storage accounts.
               If you are seeing this warning, you should separate your tenant and username values,
               as this support will be deprecated in the near future. 
            '''
      warnings.warn(msg, UserWarning)
      password = username
      tenant, username  = tenant.split(':')
      warnings.warn('Trying tenant {}, username {} and password {}'.format(tenant, username, password), UserWarning)
      

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

  def __init__(self, sparkcontext, credentials, name=None, public=False, swift2d_driver='com.ibm.stocator.fs.ObjectStoreFileSystem'):
    '''
    sparkcontext:  a SparkContext object.

    credentials:  a dictionary with the following required keys:
      
      auth_url
      project_id (or projectId)
      user_id (or userId)
      password
      region
      name  #[optional, to be deprecated] The name of the configuration.

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
        warnings.warn('credentials["name"] key will be deprecated. Use the "name" argument in object contructor', UserWarning)


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
