from typing import List
from ..domain.item import Item


class ItemLoaderRequest:

    def __init__(self, data: str):
        self.data = data


class ItemLoaderResponse:

    def __init__(self, items: List[Item]):
        self.items = items


class ItemLoaderUseCase:

    def load_items(req: ItemLoaderRequest) -> ItemLoaderResponse: ...
