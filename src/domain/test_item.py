import unittest

from .item import Item


class TestItem(unittest.TestCase):
    def setUp(self):
        self.ITEM1 = Item(
                name='Wolf Pelt',
                )
        self.ITEM2 = Item(
                name='Wolf Pelt',
                weight=8,
                price=30
                )
        self.ITEM3 = Item(
                name='Wolf Pelt (Fine)',
                weight=8,
                price=60
                )

    def test_eq(self):
        self.assertTrue(self.ITEM1 == Item('Wolf Pelt'))
        self.assertFalse(self.ITEM1 == self.ITEM2)

    def test_MakeDict(self):
        d = {}
        d[self.ITEM1] = 2
        d[self.ITEM2] = 1
        d[self.ITEM3] = 1
        self.assertEqual(
                d,
                Item.MakeDict([self.ITEM1, Item('Wolf Pelt'), self.ITEM2, self.ITEM3])
                )
