1.0.1 (2017-10-11)
====================

 - [NEW] Support for Bluemix Cloud Object Storage (COS)
 

1.0.0 (2017-07-19)
====================

 - [NEW] Support for Cloud Object Storage (COS)


0.0.8.1 (2017-06-14)
====================

 - [NEW] Build universal python 2 / python 3 wheel


0.0.8 (2017-06-13)
====================

 - [NEW] Support for Python 3
 - [DEPRECATED] The bluemix2 and softlayer2 classes were removed.

0.0.6 (2017-01-25)
====================

 - [FIXED] Connection to Softlayer Object Storage with 'swift' protocol removed in favor of all 'swift2d'
 - [WARNING] The original 'swift' protocol is no longer used. Attempts have been made not to break any code.


0.0.6 (2016-10-19)
====================

- [FIXED] By default, the ".public" Hadoop Configuration property is set to False.

0.0.5 (2016-10-18)
====================

- [NEW] Raises exception when swift (version 1) URL contains an underscore.

0.0.4 (2016-10-17)
====================

- [NEW] Separates the configuration name from the credentials
- [WARNING] The credentials['name'] key will be deprecated in the future.
- [NEW] Handles camelCase in credentials dictionary.

0.0.3 (2016-07-18)
====================

- Problem with uploading to PyPI. Trying again.

0.0.2 (2016-07-18)
====================

- [NEW] Adds option to set 'public' configuration during instantiation.

0.0.1 (2016-05-17)
====================

- [NEW] Adds automatic setting of swift2d driver (configurable).


0.0.1b0 (2016-03-17)
====================

- [NEW] Added support for Stocator driver to connect to Swift Object Stores

0.0.1a1 (2016-03-02)
====================

- [NEW] Added Initial code generate Swift URLs
