from typing import List, Optional

from ..domain.item import Item, ItemStorage
from ..domain.recipe import Recipe, RecipeStorage


class MemoryItemStorage(ItemStorage):

    def __init__(self, data=None):
        self.storage = []
        if data:
            for item in data:
                self.storage.append(item)

    def add_item(self, i: Item, unique: bool = False) -> bool:
        if unique:
            if i in self.storage:
                return False
        self.storage.append(i)
        return True

    def find_item(self, name: str) -> Optional[Item]:
        found = list(filter(lambda x: x.name == name, self.storage))
        if found != []:
            return found[0]

    def item_count(self, i: Item) -> int:
        return self.storage.count(i)

    def del_item(self, i: Item, count: int = 1) -> bool:
        if self.item_count(i) < count:
            return False
        else:
            for counter in range(count):
                self.storage.remove(i)
            return True

    def items_list(self) -> List[Item]:
        return self.storage


class MemoryRecipeStorage(RecipeStorage):

    def __init__(self, data=None):
        self.storage: List[Recipe] = []
        if data:
            for recipe in data:
                self.storage.append(recipe)

    def add_recipe(self, r: Recipe) -> bool:
        if r in self.storage:
            return False
        else:
            self.storage.append(r)
            return True

    def find_recipes(self, name: str) -> List[Recipe]:
        return [r for r in self.storage if name in list(map(lambda x: x.name, r.items))]

    def get_recipes(self, i: Item) -> List[Recipe]:
        return [r for r in self.storage if i in r.items]
