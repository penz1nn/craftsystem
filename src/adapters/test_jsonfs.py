import json
from os import remove
import unittest

from .jsonfs import JsonItemLoader, ItemLoaderRequest
from ..domain.item import Item
from ..domain.magic_item import Archetype, MagicItem
from ..domain.alchemy import AlchemyEffect, AlchemyIngredient, Potion
from ..domain.alchemy_solutions import AlchemySolution


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

    def test(self):
        j = JsonItemLoader()
        req = ItemLoaderRequest(self.filename)
        items = j.load_items(req).items
        remove(self.filename)
        self.assertEqual(self.items, items)
        for i in self.items:
            self.assertTrue(i in items)
