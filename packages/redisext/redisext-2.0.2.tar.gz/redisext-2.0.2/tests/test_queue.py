from __future__ import absolute_import

import redisext.queue
import redisext.serializer

from . import fixture


class Queue(redisext.queue.Queue):
    CONNECTION = fixture.Connection
    KEY = 'queue'
    SERIALIZER = redisext.serializer.Pickle


class QueueTestCase(fixture.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_single_push_to_queue(self):
        item = 1
        self.queue.push(item)
        self.assertEqual(self.queue.pop(), item)

    def test_multiple_push_to_queue(self):
        data = [1, 2, 3]
        for item in data:
            self.queue.push(item)
        for item in data:
            self.assertEqual(self.queue.pop(), item)

    def test_empty_counter(self):
        self.assertIsNone(self.queue.pop())

    def test_size(self):
        self.queue.push(1)
        self.assertEqual(self.queue.size(), 1)

    def test_zero_size(self):
        self.assertEqual(self.queue.size(), 0)

    def test_items(self):
        self.queue.push(1)
        self.queue.push(2)
        self.assertEqual(self.queue.items(), [2, 1])

    def test_empty_items(self):
        self.assertEqual(self.queue.items(), [])


class PriorityQueue(redisext.queue.PriorityQueue):
    CONNECTION = fixture.Connection
    KEY = 'priority_queue'
    SERIALIZER = redisext.serializer.Pickle


class PriorityQueueTestCase(fixture.TestCase):
    def setUp(self):
        self.priority_queue = PriorityQueue()

    def test_push_to_priority_queue(self):
        data = [('a', 1), ('b', 3), ('c', 3)]
        for item in data:
            self.priority_queue.push(*item)
        self.assertEqual(self.priority_queue.pop(), 'a')
        self.assertIn(self.priority_queue.pop(), ['b', 'c'])
        self.assertIn(self.priority_queue.pop(), ['b', 'c'])

    def test_unordered_push_to_priority_queue(self):
        data = [('a', 3), ('b', 2), ('c', 1)]
        for item in data:
            self.priority_queue.push(*item)
        self.assertEqual(self.priority_queue.pop(), 'c')
        self.assertEqual(self.priority_queue.pop(), 'b')
        self.assertEqual(self.priority_queue.pop(), 'a')


class KeyPickleQueue(redisext.queue.Queue):
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Pickle


class KeyQueueTestCase(fixture.KeyTestCase):
    STORAGE = KeyPickleQueue
