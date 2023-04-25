from typing import List
from ..domain.recipe import Recipe


class RecipeLoaderRequest:

    def __init__(self, data: str):
        self.data = data


class RecipeLoaderResponse:

    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes


class RecipeLoaderUseCase:

    def load_recipes(req: RecipeLoaderRequest) -> RecipeLoaderResponse: ...
