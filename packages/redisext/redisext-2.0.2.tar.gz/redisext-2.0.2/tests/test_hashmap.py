from __future__ import absolute_import

import redisext.hashmap
import redisext.key
import redisext.serializer

from . import fixture


class HashMap(redisext.hashmap.HashMap):
    CONNECTION = fixture.Connection
    KEY = 'key'
    SERIALIZER = redisext.serializer.Pickle


class HashMapTestCase(fixture.TestCase):
    def setUp(self):
        self.hashmap = HashMap()

    def test_single_put_into_hashmap(self):
        key, value = 'key1', 'value1'
        self.hashmap.set(key, value)
        self.assertEqual(self.hashmap.get(key), value)

    def test_single_removal_from_hashmap(self):
        key, value = 'key1', 'value1'
        self.hashmap.set(key, value)
        self.hashmap.remove(key)
        self.assertIsNone(self.hashmap.get(key))

    def test_multiple_put_and_removal_into_hashmap(self):
        data = {'key1': 'value1', 'key2': 'value2'}
        for key, value in data.items():
            self.hashmap.set(key, value)
            self.assertEqual(self.hashmap.get(key), value)
            self.hashmap.remove(key)
            self.assertIsNone(self.hashmap.get(key))

    def test_empty_hashmap(self):
        self.assertIsNone(self.hashmap.get('non-esixsted'))


class Map(redisext.hashmap.Map, redisext.key.Key):
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Pickle


class MapTestCase(fixture.TestCase):
    def test_multiple_map_set(self):
        data = {'map_key1': 'value1', 'map_key2': 'value2'}
        for key, value in data.items():
            Map(key).set(value)
            self.assertEqual(Map(key).get(), value)

    def test_empty_map(self):
        key, value = 'key1', 'value1'
        Map(key).set(value)
        Map(key).remove()
        self.assertIsNone(Map(key).get())

    def test_exists_method_for_failure(self):
        self.assertFalse(Map('key').exists())

    def test_exists_method_for_success(self):
        key = 'key'
        Map(key).set('')
        self.assertTrue(Map(key).exists())

    def test_random_key(self):
        key = 'key'
        Map(key).set('')
        self.assertEqual(Map().connect_to_master().randomkey(), key)

    def test_rename_key(self):
        key, newkey, value = 'key', 'key1', '_'
        Map(key).set(value)
        self.assertTrue(Map(key).rename(newkey))
        self.assertEqual(Map(newkey).get(), value)

    def test_rename_unexisted_key(self):
        key, newkey, value = 'key', 'key1', '_'
        Map(newkey).set(value)
        self.assertFalse(Map(key).rename(newkey))
        self.assertEqual(Map(newkey).get(), value)


class NumericMap(redisext.hashmap.Map):
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Numeric
    KEY = 'key1'


class NumericMapTestCase(fixture.TestCase):
    def setUp(self):
        self.numeric_map = NumericMap()

    def test_incr(self):
        self.numeric_map.incr()
        self.assertEqual(self.numeric_map.get(), 1)

    def test_decr(self):
        self.numeric_map.incr()
        self.numeric_map.decr()
        self.assertEqual(self.numeric_map.get(), 0)
