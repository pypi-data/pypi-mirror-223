from __future__ import absolute_import

import redisext.counter
import redisext.serializer

from . import fixture

REDIS_DSN = 'redis://{}:{}/{}'.format(
    fixture.REDIS_HOST,
    fixture.REDIS_PORT,
    fixture.REDIS_DB)


class Counter(redisext.counter.Counter):
    KEY = 'testkey'
    CONNECTION = REDIS_DSN
    SERIALIZER = redisext.serializer.Numeric


class DSNCounterTestCase(fixture.TestCase):
    def setUp(self):
        self.counter = Counter()

    def test_single_increment(self):
        self.counter.incr()
        self.assertEquals(self.counter.get(), 1)
