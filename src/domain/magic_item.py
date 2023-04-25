from typing import List, Optional

from .item import Item
from .magic_archetype import Archetype


class MagicItem(Item):
    archetypes: Optional[List[Archetype]]

    def __init__(
            self,
            name: str,
            archetypes: List[Archetype] = [],
            weight=0,
            price=0
            ):
        super().__init__(name, weight, price)
        self.archetypes = archetypes

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
                    'name': self.name,
                    'archetypes': self.archetypes
                })
        return d
