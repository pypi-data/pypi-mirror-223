from __future__ import absolute_import

import redisext.counter
import redisext.key
import redisext.serializer

from . import fixture


class ExpireCounter(redisext.counter.Counter, redisext.key.Expire):
    EXPIRE = 60
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Numeric


class ExpireCounterTestCase(fixture.TestCase):
    def setUp(self):
        self.counter = ExpireCounter('key')
        self.counter.incr()
        self.counter.expire()

    def test_expire(self):
        self.assertTrue(60 >= self.counter.ttl() > 0)

    def test_persist(self):
        self.counter.persist()
        self.assertEqual(self.counter.ttl(), -1)


class UnspecifiedExpireCounter(redisext.counter.Counter, redisext.key.Expire):
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Numeric


class UnspecifiedExpireCounterTestCase(fixture.TestCase):
    def setUp(self):
        self.counter = UnspecifiedExpireCounter('key')

    def test_expire_unspecified(self):
        self.counter.incr()
        with self.assertRaises(ValueError):
            self.counter.expire()

    def test_expire_specified(self):
        self.counter.incr()
        self.counter.expire(60)
        self.assertTrue(60 >= self.counter.ttl() > 0)
