from __future__ import absolute_import

import redisext.pool
import redisext.serializer

from . import fixture


class Pool(redisext.pool.Pool):
    CONNECTION = fixture.Connection
    KEY = 'key'
    SERIALIZER = redisext.serializer.Pickle


class PoolTestCase(fixture.TestCase):
    def setUp(self):
        self.pool = Pool()
        self.data = [1, 2, 3, 4, {'a': 5}]
        self.length = len(self.data)
        for item in self.data:
            self.pool.push(item)

    def test_pool_single_pop(self):
        self.assertIn(self.pool.pop(), self.data)

    def test_pool_multiple_pop(self):
        for x in range(self.length):
            self.assertIn(self.pool.pop(), self.data)

    def test_pool_members(self):
        members = self.pool.members()
        self.assertTrue(all(m in members for m in self.data))

    def test_pool_contains(self):
        self.assertTrue(self.pool.contains(1))

    def test_pool_contains_fail(self):
        self.assertFalse(self.pool.contains(6))


class EmptyPoolTestCase(fixture.TestCase):
    def test_empty_pool(self):
        self.assertIsNone(Pool().pop())

    def test_empty_pool_members(self):
        self.assertEqual(Pool().members(), [])


class KeyPicklePool(redisext.pool.Pool):
    CONNECTION = fixture.Connection
    SERIALIZER = redisext.serializer.Pickle


class KeyPoolTestCase(fixture.KeyTestCase):
    STORAGE = KeyPicklePool


class SortedSet(redisext.pool.SortedSet):
    CONNECTION = fixture.Connection
    KEY = 'key'
    SERIALIZER = redisext.serializer.Pickle


class SortedSetTestCase(fixture.TestCase):
    def setUp(self):
        self.data = {'string1': 0, 'string2': 1, 'string3': 2, 'string4': 3}
        self.sortedset = SortedSet()
        for element, score in self.data.items():
            self.sortedset.add(element, score)

    def test_sortedset_multiple_add(self):
        self.assertEquals(self.sortedset.length(0, 3), 4)

    def test_sortedset_multiple_rem(self):
        self.assertTrue(self.sortedset.rem('string1'))

    def test_sortedset_element_availability(self):
        element, score = next(iter(self.data.items()))
        self.assertTrue(self.sortedset.contains(element))

    def test_sortedset_members(self):
        expected_members = sorted(self.data.keys(), reverse=True)
        self.assertEqual(self.sortedset.members(), expected_members)

    def test_sortedset_members_with_scores(self):
        expected_members = sorted(self.data.items(), reverse=True)
        expected_members = [(s, e) for e, s in expected_members]
        self.assertEqual(self.sortedset.members(with_scores=True), expected_members)

    def test_sortedset_truncated_members(self):
        self.sortedset.truncate(2)
        truncated = sorted(self.data.keys(), reverse=True)[:-2]
        self.assertEqual(self.sortedset.members(), truncated)

    def test_sortedset_clean(self):
        self.sortedset.clean()
        self.assertEqual(self.sortedset.members(), [])

    def test_sortedset_members_by_score(self):
        expected = ['string2', 'string3']
        self.assertEqual(self.sortedset.members_by_score(1, 2), expected)

    def test_sortedset_members_by_score_with_scores(self):
        expected = [(1., 'string2'), (2., 'string3')]
        self.assertEqual(self.sortedset.members_by_score(1, 2, with_scores=True), expected)

    def test_sortedset_clean_by_score(self):
        self.sortedset.clean_by_score(0, 2)
        expected = ['string4']
        self.assertEqual(self.sortedset.members(), expected)


class EmptySortedSetTestCase(fixture.TestCase):
    def test_empty_sorted_set(self):
        self.assertEqual(SortedSet().members(), [])
