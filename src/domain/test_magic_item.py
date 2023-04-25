import unittest

from .magic_archetype import Archetype
from .magic_item import MagicItem


class TestMagicItem(unittest.TestCase):

    def setUp(self):
        self.a1 = Archetype('Magicka')
        self.a2 = Archetype('Life')
        self.mi1 = MagicItem(
                name='Ancient Text',
                archetypes=[self.a1, self.a2],
                )
        self.mi2 = MagicItem(
                name='Ancient Text',
                archetypes=[self.a2]
                )

    def test_eq(self):
        self.assertEqual(self.mi1, MagicItem(
            'Ancient Text',
            [Archetype('Magicka'), Archetype('Life')]
            ))
        self.assertNotEqual(self.mi1, MagicItem('Magic Apple', [self.a1]))
        self.assertNotEqual(self.mi1, self.mi2)

    def test_MakeDict(self):
        d = {}
        d[self.mi1] = 2
        d[self.mi2] = 1
        self.assertEqual(
                d,
                MagicItem.MakeDict([self.mi1, self.mi1, self.mi2])
                )
