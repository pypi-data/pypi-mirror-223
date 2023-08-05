Redisext
========

.. image:: https://travis-ci.org/mylokin/redisext.svg?branch=master
   :target: https://travis-ci.org/mylokin/redisext

.. image:: https://coveralls.io/repos/mylokin/redisext/badge.svg?branch=master
   :target: https://coveralls.io/r/mylokin/redisext?branch=master

.. image:: https://img.shields.io/pypi/wheel/redisext.svg
   :target: https://pypi.python.org/pypi/redisext/

.. image:: https://img.shields.io/pypi/dm/redisext.svg
   :target: https://crate.io/packages/redisext/

Documentation
-------------

Documentation is available at https://pythonhosted.org/redisext/.

Example
-------

Data model example:

.. code-block:: python

   import redisext.backend.redis
   import redisext.hashmap
   import redisext.serializer


   class Connection(redisext.backend.redis.Connection):
       MASTER = {'host': 'localhost', 'port': 6379, 'db': 0}


   class SeriousStats(redisext.hashmap.Map):
       CONNECTION = Connection
       SERIALIZER = redisext.serializer.Numeric
