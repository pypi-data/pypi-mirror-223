from __future__ import absolute_import

import os
import unittest

import redisext.backend.abc
import redisext.backend.redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


class Connection(redisext.backend.abc.IConnection):
    MASTER = {'host': REDIS_HOST, 'port': REDIS_PORT, 'db': 0}


class IConnectionTestCase(unittest.TestCase):
    def test_abstract_connection(self):
        with self.assertRaises(NotImplementedError):
            Connection.connect_to_master()


class ReplicatedConnection(redisext.backend.redis.Connection):
    MASTER = {'host': REDIS_HOST, 'port': REDIS_PORT, 'db': 0}
    SLAVE = {'host': REDIS_HOST, 'port': REDIS_PORT, 'db': 1}


class ReplicatedConnectionTestCase(unittest.TestCase):
    def tearDown(self):
        ReplicatedConnection.connect_to_master().flushdb()
        ReplicatedConnection.connect_to_slave().flushdb()

    def test_slave(self):
        ReplicatedConnection.connect_to_master().set('key', 'value')
        self.assertIsNone(ReplicatedConnection.connect_to_slave().get('key'))

    def test_pipeline(self):
        self.assertIsNotNone(ReplicatedConnection.connect_to_master().pipeline())

    def test_pipeline_transaction(self):
        self.assertIsNotNone(ReplicatedConnection.connect_to_master().pipeline(transaction=False))
