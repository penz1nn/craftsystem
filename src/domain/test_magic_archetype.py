import unittest

from .magic_archetype import Archetype

a1 = Archetype(
        name='Poison',
        )

a2 = Archetype(
        name='Life'
        )


class TestArchetype(unittest.TestCase):

    def setUp(self):
        pass

    def test_eq(self):
        self.assertEqual(a1, Archetype('Poison'))
        self.assertNotEqual(a1, a2)

    def test_hashable(self):
        d = {a1: 2}
        d[a1] = 1
        d[a2] = 3
        self.assertEqual(d[a1], 1)
        self.assertEqual(d[a2], 3)
