import json

from ..usecase.item_loader import ItemLoaderRequest, ItemLoaderResponse, ItemLoaderUseCase
from ..usecase.recipe_loader import RecipeLoaderRequest, RecipeLoaderUseCase, RecipeLoaderResponse


class JsonItemLoader(ItemLoaderUseCase):

    def __init__(self):
        self.items = []

    def load_items(self, req: ItemLoaderRequest) -> ItemLoaderResponse:
        filename = req.data
        with open(filename) as file:
            data = json.load(file)
        # self.data = data
        for item_type in data:
            self.load_part(item_type, data[item_type])
        return ItemLoaderResponse(self.items)

    def load_part(self, item_type: str, items):
        for i in items:
            i['type'] = item_type
            self.items.append(self.Item_from_dict(i))


class JsonRecipeLoader(RecipeLoaderUseCase):

    def __init__(self):
        self.recipes = []

    def load_recipes(self, req: RecipeLoaderRequest) -> RecipeLoaderResponse:
        filename = req.data
        with open(filename) as file:
            data = json.load(file)
        for recipe_data in data:
            r = self.Recipe_from_dict(recipe_data)
            self.recipes.append(r)
        return RecipeLoaderResponse(self.recipes)
