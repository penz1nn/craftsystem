from copy import copy
from typing import List

from ..domain.item import Item, ItemStorage
from ..domain.recipe import Recipe, RecipeStorage, ProductionCondition
from ..domain.alchemy_solutions import AlchemySolution


class CrafterRequest:

    def __init__(
            self,
            item_name: str,
            number: int = 1
            ):
        self.item_name = item_name
        self.number = number


class CrafterResponse:

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
        self.add_alchemy_solutions_recipes()

    def add_alchemy_solutions_recipes(self):
        for item in self.inventory.items_list():
            if isinstance(item, AlchemySolution):
                for i in range(6):
                    if i < 5:
                        self.recipe_book.add_recipe(
                                Recipe(
                                    items=[AlchemySolution(
                                        name=item.name,
                                        archetypes=item.archetypes,
                                        potency=i+2
                                        )],
                                    ingredients=[
                                        AlchemySolution(
                                            name=item.name,
                                            archetypes=item.archetypes,
                                            potency=i + 1
                                            )
                                        ]*3,
                                    conditions=[]
                                    )
                                )
                    if i > 0:
                        self.recipe_book.add_recipe(
                                Recipe(
                                    items=[AlchemySolution(
                                        name=item.name,
                                        archetypes=item.archetypes,
                                        potency=i
                                        )] * 2,
                                    ingredients=[
                                        AlchemySolution(
                                            name=item.name,
                                            archetypes=item.archetypes,
                                            potency=i + 1
                                            )
                                        ],
                                    conditions=[]
                                    )
                                )

    def add_condition(self, req: CrafterRequest) -> CrafterResponse:
        """
        add a Crafting Condition (name only!)
        """
        p_c = ProductionCondition(req.item_name)
        if p_c not in self.conditions:
            self.conditions.append(
                    p_c
                    )
            return CrafterResponse(True)
        else:
            return CrafterResponse(False)

    def show_inventory(self) -> CrafterResponse:
        d = Item.MakeDict(self.inventory.items_list())
        d_out = {}
        for item in d:
            d_out[str(item)] = d[item]
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

    def search_recipe(self, req: CrafterRequest) -> CrafterResponse:
        result = self.search_recipe_recursive(req.item_name)
        if result:
            return CrafterResponse(result['recipes_out'])
        else:
            return CrafterResponse(False)

    def search_recipe_recursive(self, item_name: str):
        subcrafter = CrafterUseCase(
                copy(self.inventory),
                self.recipe_book,
                self.conditions
                )
        # first look if we can craft item right away
        easy = False
        recipes = subcrafter.recipes(item_name)
        recipes_out = []
        for index, recipe in enumerate(recipes):
            can_craft = True
            requirements = recipe.ingredients_dict()
            for ingredient, required_count in requirements.items():
                if subcrafter.item_count(ingredient) < required_count:
                    can_craft = False
                    break
            if can_craft:
                easy = True
                req = CrafterRequest(item_name, index)
                subcrafter.craft(req)
                recipes_out.append(recipe)
        if easy:
            return {'subcrafter': subcrafter, 'recipes_out': recipes_out}
        # try to craft all requirements first
        else:
            for recipe in recipes:
                can_craft_all = True
                for ingredient in recipe.ingredients:
                    recursion_result = subcrafter.search_recipe_recursive(ingredient.name)
                    if recursion_result['recipes_out'] != []:
                        subcrafter = recursion_result['subcrafter']
                        recipes_out.extend(recursion_result['recipes_out'])
                    else:
                        can_craft_all = False
                        recipes_out = []
                        break
                if can_craft_all:
                    recipes_out.append(recipe)
        return {'subcrafter': subcrafter, 'recipes_out': recipes_out}
