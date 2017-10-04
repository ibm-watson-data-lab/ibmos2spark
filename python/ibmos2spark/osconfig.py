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

DEFAULT_SERVICE_NAME = "service"

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


class CloudObjectStorage(object):

    def __init__(self, sparkcontext, credentials, configuration_name='', cos_type='softlayer_cos', auth_method='api_key', bucket_name=''):

        '''
        This class allows you to connect to an IBM cloud object storage (COS) instance. It also support connecting to an IBM COS instance
        that is being hosted on bluemix.

        sparkcontext:  a SparkContext object.

        credentials:  a dictionary with the required keys to connect to an IBM COS. The required keys differ according
            to the type of COS.
            - for COS type "softlayer_cos" the following key are required:
              * endpoint
              * access_key
              * secret_key
            - for COS type "bluemix_cos", here are the required/optional key:
              * endpoint [required]
              * service_id [required]
              * api_key OR iam_token depends on the selected authorization method (auth_method) [required]
              * iam_service_endpoint [optional] (default: https://iam.ng.bluemix.net/oidc/token)
              * v2_signer_type [optional]

        configuration_name [optional]: string that identifies this configuration. You can
            use any string you like. This allows you to create
            multiple configurations to different Object Storage accounts.
            if a configuration name is not passed the default one will be used "service".

        cos_type [optional]: string that identifies the type of COS to connect to. The supported types of COS
            are "softlayer_cos" and "bluemix_cos". "softlayer_cos" will be chosen as default if no cos_type is passed.

        auth_method [optional]: string that identifies the type of authorization to use when connecting to an IBM COS. This parameter
            is not reqired for softlayer_cos but only needed for bluemix_cos. Two options can be chosen for this params
            "api_key" or "iam_token". "api_key" will be chosen as default if the value is not set.

        bucket_name [optional]:  string that identifies the defult
            bucket nameyou want to access files from in the COS service instance.
            If this value is not specified, you need to pass it when
            you use the url function.

        '''
        # check if all required values are availble
        self._validate_input(credentials, cos_type, auth_method)

        self.bucket_name = bucket_name
        self.conf_name = configuration_name

        # setup config
        prefix = "fs.cos"

        if (configuration_name):
            prefix = "{}.{}".format(prefix, configuration_name)
        else:
            prefix = prefix + "." + DEFAULT_SERVICE_NAME

        hconf = sparkcontext._jsc.hadoopConfiguration()
        hconf.set(prefix + ".endpoint", credentials['endpoint'])

        # softlayer cos case
        if (cos_type == "softlayer_cos"):
            hconf.set(prefix + ".access.key", credentials['access_key'])
            hconf.set(prefix + ".secret.key", credentials['secret_key'])

        # bluemix cos case
        elif (cos_type == "bluemix_cos"):
            hconf.set(prefix + ".iam.service.id", credentials['service_id'])
            if (auth_method == "api_key"):
                hconf.set(prefix + ".iam.api.key", credentials['api_key'])
            elif (auth_method == "iam_token"):
                hconf.set(prefix + ".iam.token", credentials['iam_token'])

            if (credentials.get('iam_service_endpoint')):
                hconf.set(prefix + ".iam.endpoint", credentials['iam_service_endpoint'])

            if (credentials.get('v2_signer_type')):
                hconf.set(prefix + ".v2.signer.type", credentials['v2_signer_type'])

    def _validate_input(self, credentials, cos_type, auth_method):
        required_key_softlayer_cos = ["endpoint", "access_key", "secret_key"]
        required_key_list_iam_api_key = ["endpoint", "api_key", "service_id"]
        required_key_list_iam_token = ["endpoint", "iam_token", "service_id"]

        def _get_required_keys(cos_type, auth_method):
            if (cos_type == "bluemix_cos"):
                if (auth_method == "api_key"):
                    return required_key_list_iam_api_key
                elif (auth_method == "iam_token"):
                    return required_key_list_iam_token
                else:
                    raise ValueError("Invalid input: auth_method. auth_method is optional but if set, it should have one of the following values: api_key, iam_token")
            elif (cos_type == "softlayer_cos"):
                return required_key_softlayer_cos
            else:
                raise ValueError("Invalid input: cos_type. cos_type is optional but if set, it should have one of the following values: softlayer_cos, bluemix_cos")

        # check keys
        required_key_list = _get_required_keys(cos_type, auth_method)

        for i in range(len(required_key_list)):
            key = required_key_list[i]
            if (key not in credentials):
                raise ValueError("Invalid input: credentials. {} is required!".format(key))

    def url(self, object_name, bucket_name=''):
        bucket_name_var = ''
        service_name = DEFAULT_SERVICE_NAME

        # determine the bucket to use
        if (bucket_name):
            bucket_name_var = bucket_name
        elif (self.bucket_name):
            bucket_name_var = self.bucket_name
        else:
            raise ValueError("Invalid input: bucket_name is required!")

        # use service name that we set up hadoop config for
        if (self.conf_name):
            service_name = self.conf_name

        return "cos://{}.{}/{}".format(bucket_name_var, service_name, object_name)
