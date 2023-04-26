import json
from os import remove
import unittest

from .jsonfs import JsonItemLoader, ItemLoaderRequest, JsonRecipeLoader, RecipeLoaderRequest
from ..domain.item import Item
from ..domain.magic_item import Archetype, MagicItem
from ..domain.alchemy import AlchemyEffect, AlchemyIngredient, Potion
from ..domain.alchemy_solutions import AlchemySolution
from ..domain.recipe import Recipe, ProductionCondition


testdata = """
{
    "item": [
        {
            "name": "Wolf pelt"
        }
    ],
    "magic": [
        {
            "name": "enchanted sword blade",
            "archetypes": ["shock", "poison"]
        }
    ],
    "alchemy_solution": [
        {
            "name": "Agea",
            "archetypes": ["life"],
            "potency": 3
        }
    ],
    "alchemy_ingredient": [
        {
            "name": "Nirnroot",
            "effects": [
                {
                    "name": "Damage health",
                    "is_harmful": true
                },
                {
                    "name": "Restore magicka",
                    "is_harmful": false
                },
                {
                    "name": "Invisibility"
                }
            ],
            "weight": 0.2,
            "price": 83
        }
    ],
    "potion": [
        {
            "name": "Potion of restore health",
            "effects": [
                {
                    "name": "Restore health"
                }
            ],
            "descr": "Restore 10 HP"
        }
    ]
}
"""


class TestJsonItemLoader(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_JsonItemLoader.json'
        with open(self.filename, 'w') as file:
            data = json.loads(testdata)
            json.dump(data, file)

        self.item1 = Item('Wolf pelt')

        self.item2 = MagicItem(
                name='enchanted sword blade',
                archetypes=[
                    Archetype('shock'),
                    Archetype('poison')
                    ]
                )

        self.item3 = AlchemySolution(
                name='Agea',
                archetypes=[Archetype('life')],
                potency=3
                )

        self.item4 = AlchemyIngredient(
                name='Nirnroot',
                effects=[
                    AlchemyEffect('Damage health', is_harmful=True),
                    AlchemyEffect('Restore magicka'),
                    AlchemyEffect('Invisibility')
                    ],
                weight=0.2,
                price=83
                )

        self.item5 = Potion(
                name='Potion of restore health',
                effects=[
                    AlchemyEffect('Restore health'),
                    ],
                descr='Restore 10 HP'
                )

        self.items = [
                self.item1,
                self.item2,
                self.item3,
                self.item4,
                self.item5
                ]

    def test_load_items(self):
        j = JsonItemLoader()
        req = ItemLoaderRequest(self.filename)
        items = j.load_items(req).items
        remove(self.filename)
        self.assertEqual(self.items, items)
        for i in self.items:
            self.assertTrue(i in items)


testdata_recipes = """
[
    {
        "items": [
            {
                "type": "item",
                "name": "Leather"
            }
        ],
        "ingredients": [
            {
                "type": "item",
                "name": "Wolf pelt"
            }
        ],
        "conditions": [
            {
                "name": "tanning_rack"
            }
        ]
    },
    {
        "items": [
            {
                "type": "potion",
                "name": "Potion of restore magicka",
                "effects": [
                    {
                        "name": "Restore magicka"
                    }
                ],
                "descr": "Restore 10 MP"
            }
        ],
        "ingredients": [
            {
                "type": "alchemy_ingredient",
                "name": "Nirnroot",
                "effects": [
                    {
                        "name": "Restore magicka"
                    },
                    {
                        "name": "Damage health"
                    },
                    {
                        "name": "Invisibility"
                    }
                ]
            }
        ],
        "conditions": [
            {
                "name": "alchemy"
            }
        ]
    },
    {
        "items": [
            {
                "type": "item",
                "name": "Leather strips"
            },
            {
                "type": "item",
                "name": "Leather strips"
            },
            {
                "type": "item",
                "name": "Leather strips"
            },
            {
                "type": "item",
                "name": "Leather strips"
            }
        ],
        "ingredients": [
            {
                "type": "item",
                "name": "Leather"
            }
        ],
        "conditions": [
            {
                "name": "tanning_rack"
            }
        ]
    }
]
"""


class TestJsonRecipeLoader(unittest.TestCase):

    def setUp(self):
        self.filename = 'test_JsonRecipeLoader.json'
        with open(self.filename, 'w') as file:
            data = json.loads(testdata_recipes)
            json.dump(data, file)

        self.recipe1 = Recipe(
                items=[
                    Item('Leather')
                    ],
                ingredients=[
                    Item('Wolf pelt')
                    ],
                conditions=[
                    ProductionCondition('tanning_rack')
                    ]
                )

        self.recipe2 = Recipe(
                items=[
                    Potion(
                        name='Potion of restore magicka',
                        effects=[
                            AlchemyEffect('Restore magicka')
                            ],
                        descr='Restore 10 MP'
                        )
                    ],
                ingredients=[
                    AlchemyIngredient(
                        name='Nirnroot',
                        effects=[
                            AlchemyEffect('Restore magicka'),
                            AlchemyEffect('Damage health'),
                            AlchemyEffect('Invisibility')
                            ]
                        )
                    ],
                conditions=[
                    ProductionCondition('alchemy')
                    ]
                )

        self.recipe3 = Recipe(
                items=[Item('Leather strips')] * 4,
                ingredients=[Item('Leather')],
                conditions=[ProductionCondition('tanning_rack')]
                )

        self.recipes = [
                self.recipe1,
                self.recipe2,
                self.recipe3
                ]

    def test_load_recipes(self):
        j = JsonRecipeLoader()
        req = RecipeLoaderRequest(self.filename)
        recipes = j.load_recipes(req).recipes
        remove(self.filename)
        self.assertEqual(len(self.recipes), len(recipes))
        for r in self.recipes:
            self.assertTrue(
                    r in recipes,
                    msg=str(r)
                    )
