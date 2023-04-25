import unittest

from .item import Item
from .recipe import ProductionCondition, Recipe


COND1 = ProductionCondition('tanning_rack', 'Use taning rack')
COND2 = ProductionCondition('skin', 'Use skinning')
ITEM1 = Item('Wolf Pelt')
ITEM2 = Item('Wolf Pelt (Fine)')
ITEM3 = Item('Wolf Corpse')
ITEM4 = Item('Leaher')
ITEM5 = Item('Leather strips')


class TestProductCondition(unittest.TestCase):

    def setUp(self):
        pass

    def test_eq(self):
        self.assertTrue(COND1 == ProductionCondition('tanning_rack'))
        self.assertFalse(COND1 == ProductionCondition('anvil'))
        self.assertFalse(COND1 == COND2)


class TestRecipe(unittest.TestCase):

    def setUp(self):
        self.R1 = Recipe(
                items=[ITEM1, ITEM1],
                ingredients=[ITEM2],
                conditions=[COND1],
                )
        self.R2 = Recipe(
                items=[ITEM1],
                ingredients=[ITEM3],
                conditions=[COND2]
                )
        self.R3 = Recipe(
                items=[ITEM4],
                ingredients=[ITEM1],
                conditions=[COND1]
                )
        self.R4 = Recipe(
                items=[ITEM5] * 4,
                ingredients=[ITEM4],
                conditions=[COND1]
                )

    def test_eq(self):
        recipe = Recipe(
                items=[Item('Wolf Pelt'), Item('Wolf Pelt')],
                ingredients=[Item('Wolf Pelt (Fine)')],
                conditions=[COND1],
                )
        self.assertEqual(recipe, self.R1)
        self.assertNotEqual(self.R1, self.R2)

    def test_ingredients_dict(self):
        d = {}
        d[ITEM3] = 1
        self.assertEqual(d, self.R2.ingredients_dict())

    def test_craft(self):
        items = [ITEM2]
        self.assertTrue(self.R1.craft(items, [COND1]))
        self.assertEqual(items, [ITEM1, ITEM1])
        self.assertTrue(self.R3.craft(items, [COND1]))
        self.assertEqual(items, [ITEM1, ITEM4])
        self.assertTrue(self.R4.craft(items, [COND1]))
        self.assertTrue(self.R3.craft(items, [COND1]))
        self.assertTrue(self.R4.craft(items, [COND1]))
        self.assertEqual(items, [ITEM5] * 8)
        self.assertFalse(self.R1.craft(items, [COND1]))
        self.assertEqual(items, [ITEM5] * 8)
