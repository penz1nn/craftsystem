import unittest


from .item_loader import ItemLoaderUseCase
from .item_loader import Item, MagicItem, Archetype, AlchemySolution, AlchemyEffect, AlchemyIngredient, Potion


dict1 = {
        'type': 'item',
        'name': 'Wolf pelt'
        }

dict2 = {
        'type': 'magic',
        'name': 'enchanted sword blade',
        'archetypes': ['shock', 'poison']
        }

dict3 = {
        'type': 'alchemy_solution',
        'name': 'Agea',
        'archetypes': ['life'],
        'potency': 3
        }

dict4 = {
        'type': 'alchemy_ingredient',
        'name': 'Nirnroot',
        'effects': [
            {
                'name': 'Damage health',
                'is_harmful': True
                },
            {
                'name': 'Restore magicka',
                'is_harmful': False
                },
            {
                'name': 'Invisibility',
                'is_harmful': False
                }
            ],
        'weight': 0.2,
        'price': 83
        }

dict5 = {
        'type': 'potion',
        'name': 'Potion of restore health',
        'effects': [
            {
                'name': 'Restore health',
                'is_harmful': False
                }
            ],
        'descr': 'Restore 10 HP'
        }


class TestItemLoaderUseCase(unittest.TestCase):

    def setUp(self):
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

    def test_Item_from_dict(self):
        self.assertEqual(
                ItemLoaderUseCase.Item_from_dict(dict1),
                self.item1
                )
        self.assertEqual(
                ItemLoaderUseCase.Item_from_dict(dict2),
                self.item2
                )
        self.assertEqual(
                ItemLoaderUseCase.Item_from_dict(dict3),
                self.item3,
                msg=str(self.item3.to_dict()) + '!=' + str(ItemLoaderUseCase.Item_from_dict(dict3).to_dict())
                )
        self.assertEqual(
                ItemLoaderUseCase.Item_from_dict(dict4),
                self.item4,
                msg=str(self.item4.to_dict()) + '!=' + str(ItemLoaderUseCase.Item_from_dict(dict4).to_dict())
                )
        self.assertEqual(
                ItemLoaderUseCase.Item_from_dict(dict5),
                self.item5,
                msg=str(self.item5.to_dict()) + '!=' + str(ItemLoaderUseCase.Item_from_dict(dict5).to_dict())
                )
