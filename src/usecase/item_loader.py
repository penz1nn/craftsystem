from typing import List, Optional
from ..domain.item import Item
from ..domain.magic_item import Archetype, MagicItem
from ..domain.alchemy import AlchemyEffect, AlchemyIngredient, Potion
from ..domain.alchemy_solutions import AlchemySolution


class ItemLoaderRequest:

    def __init__(self, data: str):
        self.data = data


class ItemLoaderResponse:

    def __init__(self, items: List[Item]):
        self.items = items


class ItemLoaderUseCase:

    def load_items(self, req: ItemLoaderRequest) -> ItemLoaderResponse: ...

    @classmethod
    def Item_from_dict(cls, item_data: dict) -> Item:
        if not item_data or 'type' not in item_data:
            return Item('Unknown item')
        item_type = item_data['type']
        if item_type == 'item':
            return Item(
                    name=item_data['name'],
                    weight=item_data.get('weight', 0),
                    price=item_data.get('price', 0)
                    )
        elif item_type == 'magic' or item_type == 'alchemy_solution':
            archetypes = []
            for a in item_data['archetypes']:
                archetypes.append(Archetype(a))
            if item_type == 'magic':
                return MagicItem(
                        name=item_data['name'],
                        archetypes=archetypes,
                        weight=item_data.get('weight', 0),
                        price=item_data.get('price', 0)
                        )
            elif item_type == 'alchemy_solution':
                return AlchemySolution(
                        name=item_data['name'],
                        archetypes=archetypes,
                        potency=item_data['potency'],
                        weight=item_data.get('weight', 0.1),
                        price=item_data.get('price', 0)
                        )
        elif item_type == 'alchemy_ingredient' or item_type == 'potion':
            effects = []
            for e in item_data['effects']:
                effects.append(AlchemyEffect(
                    name=e['name'],
                    is_harmful=e.get('is_harmful', False),
                    descr=e.get('descr', '')
                    ))
            if item_type == 'alchemy_ingredient':
                return AlchemyIngredient(
                        name=item_data['name'],
                        weight=item_data.get('weight', 0),
                        effects=effects,
                        price=item_data.get('price', 0)
                        )
            elif item_type == 'potion':
                return Potion(
                        name=item_data['name'],
                        effects=effects,
                        weight=item_data.get('weight', 0.5),
                        price=item_data.get('price', 0),
                        descr=item_data['descr']
                        )
        else:
            return Item('Unknown item')
