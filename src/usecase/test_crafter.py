import unittest


from .crafter import CrafterRequest, CrafterResponse, CrafterUseCase
from ..adapters.memory import MemoryItemStorage as ItemStorage
from ..adapters.memory import MemoryRecipeStorage as RecipeStorage
from ..domain.item import Item
from ..domain.recipe import Recipe, ProductionCondition
from ..domain.alchemy import ALCHEMY, AlchemyEffect, AlchemyIngredient, Potion
from ..domain.alchemy_solutions import Archetype, AlchemySolution


i1 = AlchemyIngredient(
        name='Nirnroot',
        effects=[
            AlchemyEffect('Restore Magicka'),
            AlchemyEffect('Damage Health'),
            AlchemyEffect('Invisibility'),
            AlchemyEffect('Fortify Conjuration')
            ]
        )
i2 = Potion(
        name='Potion of restore magicka',
        effects=[AlchemyEffect('RestoreMagicka')],
        descr='Restore 100 MP'
        )
r1 = Recipe(
        items=[i2],
        conditions=ALCHEMY,
        ingredients=[i1]
        )
c1 = ProductionCondition(
        name='tanning_rack'
        )
i3 = Item(
        name='Leather'
        )
r2 = Recipe(
        items=[i3, Item('Fur plate')],
        conditions=[c1],
        ingredients=[Item('Bear pelt')]
        )
r3 = Recipe(
        items=[i3] * 2,
        conditions=[c1],
        ingredients=[Item('Horse pelt')]
        )


class TestCrafter(unittest.TestCase):

    def setUp(self):
        self.inv = ItemStorage([
            i1, i2, i3, Item('Bear pelt'), Item('Horse pelt')
            ])
        self.rb = RecipeStorage([r1, r2, r3])

    def test_show_inventory(self):
        c = CrafterUseCase(
                ItemStorage([
                    Item('Wolf pelt'),
                    Item('Iron dagger'),
                    Item('Wolf pelt')
                    ]),
                self.rb,
                []
                )
        d = {
                'Wolf pelt': 2,
                'Iron dagger': 1
                }
        response = CrafterResponse(d)
        self.assertEqual(c.show_inventory().data, response.data)

    def test_get_recipes(self):
        c = CrafterUseCase(self.inv, self.rb, [])
        # get known recipes
        req = CrafterRequest('Leather')
        response = c.get_recipes(req)
        self.assertTrue(response.success)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(r2 in response.data)
        self.assertTrue(r3 in response.data)
        # try to get unknown recipes
        req = CrafterRequest('Feather')
        response = c.get_recipes(req)
        self.assertFalse(response.success)

    def test_get_item(self):
        c = CrafterUseCase(self.inv, self.rb, [])
        # get posessed item
        req = CrafterRequest('Leather')
        response = c.get_item(req)
        self.assertTrue(response.success)
        self.assertEqual(response.data, Item('Leather'))
        # try to get non possessed item
        req = CrafterRequest('Feather')
        response = c.get_item(req)
        self.assertFalse(response.success)

    def test_get_item_count(self):
        c = CrafterUseCase(self.inv, self.rb, [])
        # get count of item normally
        req = CrafterRequest('Leather')
        response = c.get_item_count(req)
        self.assertTrue(response.success)
        self.assertEqual(response.data, 1)
        # ask if there is sufficient items
        req = CrafterRequest('Leather', 2)
        response = c.get_item_count(req)
        self.assertFalse(response.success)
        # test with more counts
        inv = ItemStorage([i1, i1, i1, i2, i2])
        c = CrafterUseCase(inv, self.rb, [])
        req = CrafterRequest(i1.name)
        response = c.get_item_count(req)
        self.assertTrue(response.success)
        self.assertEqual(response.data, 3)

        req = CrafterRequest(i1.name, 3)
        self.assertTrue(c.get_item_count(req).success)

        req = CrafterRequest(i1.name, 4)
        self.assertFalse(c.get_item_count(req).success)

    def test_craft(self):
        # craft an item
        c = CrafterUseCase(self.inv, self.rb, [ALCHEMY])
        req = CrafterRequest(i2.name, 1)
        self.assertTrue(c.craft(req).success)
        self.assertEqual(c.get_item_count(req).data, 2)
        # try to craft without a condition
        c = CrafterUseCase(self.inv, self.rb, [])
        self.assertFalse(c.craft(req).success)
        # try to craft without items
        c = CrafterUseCase(
                ItemStorage([i3]),
                self.rb,
                [ALCHEMY]
                )
        self.assertFalse(c.craft(req).success)

    def test_add_alchemy_solutions_recipes(self):
        # NOTE: may be an insufficient check?
        item = AlchemySolution(
                name='Agea',
                archetypes=[
                    Archetype('magicka')
                    ],
                potency=1
                )
        inv = ItemStorage([item])
        c = CrafterUseCase(inv, self.rb, [])
        req = CrafterRequest(item.name)
        resp = c.get_recipes(req)
        self.assertTrue(resp.success)
        self.assertEqual(len(resp.data), 10)

    def test_add_condition(self):
        # NOTE: also depends on method CrafterUseCase.craft
        c = CrafterUseCase(self.inv, self.rb, [])
        # add condition
        req = CrafterRequest(ALCHEMY.name)
        self.assertTrue(c.add_condition(req).success)
        # try to add it again
        self.assertFalse(c.add_condition(req).success)
        # craft item which requires that condition
        req = CrafterRequest(i2.name, 1)
        self.assertTrue(c.craft(req).success)
