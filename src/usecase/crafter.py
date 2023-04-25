from typing import List

from ..domain.item import Item, ItemStorage
from ..domain.recipe import Recipe, RecipeStorage, ProductionCondition


class CrafterRequest:

    def __init__(
            self,
            item_name: str,
            number: int = 1
            ):
        self.item_name = item_name
        self.number = number


class CrafterResponse:
    success: bool

    def __init__(
            self,
            data
            ):
        if data:
            self.success = True
            self.data = data
        else:
            self.success = False
            self.data = None


class CrafterUseCase:

    def __init__(
            self,
            inventory: ItemStorage,
            recipe_book: RecipeStorage,
            conditions: List[ProductionCondition]
            ):
        self.inventory = inventory
        self.recipe_book = recipe_book
        self.conditions = conditions

    def show_inventory(self) -> CrafterResponse:
        d = Item.MakeDict(self.inventory.items_list())
        d_out = {}
        for item in d:
            d_out[item.name] = d[item]
        return CrafterResponse(d_out)

    def item(self, name: str) -> Item:
        return self.inventory.find_item(name)

    def recipes(self, name: str) -> List[Recipe]:
        return self.recipe_book.find_recipes(name)

    def item_count(self, item: Item) -> int:
        if not item:
            return 0
        else:
            return self.inventory.item_count(item)

    def get_item_count(self, req: CrafterRequest) -> CrafterResponse:
        i = self.item(req.item_name)
        count = self.item_count(i)
        if count < req.number:
            return CrafterResponse(False)
        else:
            return CrafterResponse(count)

    def get_item(self, req: CrafterRequest) -> CrafterResponse:
        i = self.item(req.item_name)
        if i:
            return CrafterResponse(i)
        else:
            return CrafterResponse(False)

    def get_recipes(self, req: CrafterRequest) -> CrafterResponse:
        r = self.recipes(req.item_name)
        if r:
            return CrafterResponse(r)
        else:
            return CrafterResponse(False)

    def craft(self, req: CrafterRequest) -> CrafterResponse:
        rcs = self.recipes(req.item_name)
        if len(rcs) < req.number - 1:
            return CrafterResponse(False)
        r: Recipe = rcs[req.number - 1]
        requirements = r.ingredients_dict()
        for i in requirements:
            if self.item_count(i) < requirements[i]:
                return CrafterResponse(False)
        for i in r.ingredients:
            self.inventory.del_item(i, requirements[i])
        for i in r.items:
            self.inventory.add_item(i)
        return CrafterResponse(r.items)
