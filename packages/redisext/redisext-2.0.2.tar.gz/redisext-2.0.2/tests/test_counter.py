from __future__ import absolute_import

import redisext.counter
import redisext.serializer

from . import fixture


class Counter(redisext.counter.Counter):
    CONNECTION = fixture.Connection
    KEY = 'key'
    SERIALIZER = redisext.serializer.Numeric


class CounterTestCase(fixture.TestCase):
    def setUp(self):
        self.counter = Counter()

    def test_single_increment(self):
        self.counter.incr()
        self.assertEquals(self.counter.get(), 1)

    def test_single_increment_by_5(self):
        self.counter.incr(5)
        self.assertEquals(self.counter.get(), 5)

    def test_multiple_increment(self):
        for x in range(10):
            self.counter.incr()
        self.assertEquals(self.counter.get(), 10)

    def test_empty_counter(self):
        self.assertIsNone(self.counter.get())
