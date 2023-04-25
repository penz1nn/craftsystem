import unittest

from .memory import MemoryItemStorage, MemoryRecipeStorage
from ..domain.item import Item
from ..domain.recipe import Recipe, ProductionCondition
from ..domain.magic_item import MagicItem
from ..domain.alchemy_solutions import AlchemySolution, Archetype
from ..domain.alchemy import ALCHEMY, AlchemyEffect, AlchemyIngredient, Potion


a1 = Archetype('Magicka')
a2 = Archetype('Shock')
item1 = AlchemySolution(
        name='Agea',
        archetypes=[a1],
        potency=1
        )
e1 = AlchemyEffect('Invisibility')
e2 = AlchemyEffect('Damage Health')
e3 = AlchemyEffect('Restore Magicka')
e4 = AlchemyEffect('Fortify Conjuration')
item2 = AlchemyIngredient(
        name='Nirnroot',
        effects=[e1, e2, e3, e4]
        )
item3 = Item('Wolf pelt')
item4 = MagicItem(name='Enchanted War Axe Head', archetypes=[a1, a2])
item5 = Potion(
        name='Potion of Restore Magicka',
        effects=[e3],
        descr='Restore 10 MP'
        )


class TestMemoryItemStorage(unittest.TestCase):

    def setUp(self):
        self.items = [item1, item2, item3, item4, item5]

    def test_init_and_list(self):
        # NOTE: may fail bcs of list order?
        storage = MemoryItemStorage(self.items)
        self.assertEqual(storage.items_list(), self.items)

    def test_add_item(self):
        storage = MemoryItemStorage([item1])
        # test add of one item
        self.assertTrue(storage.add_item(item2))
        self.assertTrue(item1 in storage.items_list())
        self.assertTrue(item2 in storage.items_list())
        self.assertEqual(len(storage.items_list()), 2)
        # test add of unique item
        self.assertTrue(storage.add_item(item3, unique=True))
        self.assertFalse(storage.add_item(item2, unique=True))
        # test add of all items
        for i in self.items:
            self.assertTrue(storage.add_item(i))
        self.assertEqual(len(storage.items_list()), 8)

    def test_item_count(self):
        storage = MemoryItemStorage(self.items)
        storage.add_item(item2)
        self.assertEqual(storage.item_count(item2), 2)
        self.assertEqual(storage.item_count(item1), 1)

    def test_find_item(self):
        storage = MemoryItemStorage([item1, item2])
        self.assertEqual(item1, storage.find_item(item1.name))
        self.assertIsNone(storage.find_item('abracadabra'))

    def test_del_item(self):
        storage = MemoryItemStorage([item1, item2, item3])
        self.assertFalse(storage.del_item(item4))
        self.assertTrue(storage.del_item(item1))
        self.assertEqual(len(storage.items_list()), 2)
        self.assertTrue(storage.del_item(item3))
        self.assertEqual(storage.items_list(), [item2])


r1 = Recipe(
        items=[item5],
        conditions=ALCHEMY,
        ingredients=[item2]
        )
r2 = Recipe(
        items=[Item('Leather')],
        conditions=[],
        ingredients=[item3]
        )
r3 = Recipe(
        items=[Item('Leather strips')] * 4,
        conditions=[],
        ingredients=[Item('Leather')]
        )
r4 = Recipe(
        items=[Item('Leather'), Item('Fur plate')],
        conditions=[],
        ingredients=[Item('Bear Pelt')]
        )
r5 = Recipe(
        items=[Item('Leather')],
        conditions=[],
        ingredients=[Item('Wolf Pelt (Poor)')] * 2
        )


class TestRecipeMemoryStorage(unittest.TestCase):

    def setUp(self):
        self.recipes = [r1, r2, r3, r4, r5]

    def test_init(self):
        # NOTE: contains logic specific to this implementation of RecipeStorage
        storage = MemoryRecipeStorage(self.recipes)
        self.assertEqual(len(storage.storage), 5)

    def test_add_recipe(self):
        # NOTE: contains logic specific to this implementation of RecipeStorage
        storage = MemoryRecipeStorage()
        # add recipe normally
        self.assertTrue(storage.add_recipe(r1))
        self.assertEqual(storage.storage, [r1])
        # try to add same recipe
        self.assertFalse(storage.add_recipe(r1))

    def test_find_recipes(self):
        storage = MemoryRecipeStorage(self.recipes)
        rcs = storage.find_recipes('Leather')
        self.assertEqual(len(rcs), 3)

    def test_get_recipes(self):
        storage = MemoryRecipeStorage(self.recipes)
        rcs = storage.get_recipes(Item('Leather'))
        self.assertEqual(len(rcs), 3)
        rcs = storage.get_recipes(Item('Fur plate'))
        self.assertEqual(len(rcs), 1)
