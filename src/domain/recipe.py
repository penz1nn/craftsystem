from typing import List, Optional
from .item import Item


class ProductionCondition:
    name: str
    descr: str

    def __init__(self, name: str, descr: str = ''):
        self.name = name
        self.descr = descr

    def __eq__(self, o):
        return self.name == o.name

    def __str__(self):
        text = self.name
        if self.descr:
            text += ': ' + self.descr
        return text


class Recipe:
    items: List[Item]
    ingredients: List[Item]
    conditions: List[ProductionCondition]

    def __init__(
            self,
            items: List[Item],
            ingredients: List[Item],
            conditions: List[ProductionCondition] = [],
            ):
        self.items = items
        self.ingredients = ingredients
        self.conditions = conditions

    def ingredients_dict(self):
        return Item.MakeDict(self.ingredients)

    def __str__(self):
        d = Item.MakeDict(self.items)
        text = '['
        for i in d:
            text += str(d[i]) + ' x ' + str(i) + ', '
        text = text[:-2] + ']: '
        d = self.ingredients_dict()
        for i in d:
            text += str(d[i]) + ' x ' + str(i) + ', '
        return text[:-2] + '.'

    def to_dict(self) -> dict:
        return {
                'items': self.items,
                'ingredients': self.ingredients,
                'conditions': self.conditions
                }

    def can_craft_with(self, items: List[Item], conds: List[ProductionCondition]) -> bool:
        # check that conditions are satisfied
        for c in self.conditions:
            if c not in conds:
                return False
        # check that required items are in provided inventory
        inv = Item.MakeDict(items)
        req = self.ingredients_dict()
        for i in req:
            if inv.get(i, 0) < req[i]:
                return False
        return True

    def craft(self, items: List[Item], conds: List[ProductionCondition]) -> bool:
        if not self.can_craft_with(items, conds):
            return False
        else:
            # take required ingridients from provided inventory
            for i in self.ingredients:
                items.remove(i)
            # add crafted items
            for i in self.items:
                items.append(i)
            return True

    def __eq__(self, o):
        return self.to_dict() == o.to_dict()

    def __hash__(self):
        return hash(str(self.to_dict()))


class RecipeStorage:
    def add_recipe(self, r: Recipe) -> bool: ...
    def find_recipes(self, name: str) -> List[Recipe]: ...
    def get_recipes(self, i: Item) -> List[Recipe]: ...
