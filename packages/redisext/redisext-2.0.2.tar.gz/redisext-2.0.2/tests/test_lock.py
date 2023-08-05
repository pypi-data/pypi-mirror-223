from __future__ import absolute_import

import redisext.lock

from . import fixture


class Lock(redisext.lock.Lock):
    CONNECTION = fixture.Connection
    KEY = 'lock'


class HashMapTestCase(fixture.TestCase):
    def setUp(self):
        self.lock = Lock()

    def test_acquire(self):
        self.lock.acquire()
        self.assertTrue(self.lock.exists())

    def test_acquire_with_expiration(self):
        expiration = 10
        self.lock.acquire(expiration)
        self.assertLessEqual(self.lock.ttl(), expiration)

    def test_release(self):
        self.lock.acquire()
        self.assertTrue(self.lock.release())

    def test_fail_acquire(self):
        self.lock.acquire()
        self.assertFalse(self.lock.acquire())

    def test_fail_release(self):
        self.assertFalse(self.lock.release())
