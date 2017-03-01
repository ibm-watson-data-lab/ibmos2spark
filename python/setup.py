#!/usr/bin/env python
# Copyright (c) 2016 IBM. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
_setup.py_

Helper tool to configure access to Bluemix and Softlayer Object Store from Bluemix Spark service.

"""

from setuptools import setup, find_packages

from ibmos2spark.__info__ import __version__

setup_args = {
    'description': 'Helper tool to access Softlayer Object Store',
    'include_package_data': True,
    'install_requires': [],
    'name': 'ibmos2spark',
    'version': __version__,
    'author': 'gadamc',
    'author_email': 'adamcox@us.ibm.com',
    'url': 'https://github.com/ibm-cds-labs/ibmos2spark',
    'packages': ['ibmos2spark'],
    'classifiers': [
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development :: Libraries',
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5'
      ]
}

setup(**setup_args)
