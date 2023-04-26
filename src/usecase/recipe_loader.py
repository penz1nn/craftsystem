from typing import List
from ..domain.recipe import Recipe, ProductionCondition
from .item_loader import ItemLoaderUseCase


class RecipeLoaderRequest:

    def __init__(self, data: str):
        self.data = data


class RecipeLoaderResponse:

    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes


class RecipeLoaderUseCase:

    def load_recipes(req: RecipeLoaderRequest) -> RecipeLoaderResponse: ...

    @classmethod
    def Recipe_from_dict(cls, recipe_data: dict) -> Recipe:
        items = []
        ingredients = []
        conditions = []
        for i in recipe_data['items']:
            items.append(ItemLoaderUseCase.Item_from_dict(i))
        for i in recipe_data['ingredients']:
            ingredients.append(ItemLoaderUseCase.Item_from_dict(i))
        for c in recipe_data['conditions']:
            conditions.append(
                    ProductionCondition(
                        name=c['name'],
                        descr=c.get('descr', '')
                        )
                    )
        return Recipe(
                items=items,
                ingredients=ingredients,
                conditions=conditions
                )
