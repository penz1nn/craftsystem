from __future__ import annotations
from typing import List, Optional


class Item:
    name: str
    weight: float
    price: float

    def __init__(
            self,
            name,
            weight=0,
            price=0,
            ):
        self.name = name
        self.weight = weight
        self.price = price

    def to_dict(self):
        return {
                'name': self.name,
                'weight': self.weight,
                'price': self.price
                }

    def __eq__(self, o):
        return self.to_dict() == o.to_dict()

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self.to_dict()))

    @classmethod
    def MakeDict(cls, items: List[Item]) -> dict:
        d = {}
        for i in items:
            if i in d:
                d[i] += 1
            else:
                d[i] = 1
        return d


class ItemStorage:
    def add_item(self, i: Item, unique: bool = False) -> bool: ...
    def find_item(self, name: str) -> Optional[Item]: ...
    def item_count(self, i: Item) -> int: ...
    def del_item(self, item: Item, count: int = 1) -> bool: ...
    def items_list(self) -> List[Item]: ...
