from __future__ import annotations
from enum import Enum
from typing import List
from copy import copy

from .magic_item import MagicItem
from .magic_archetype import Archetype


class Potency(Enum):
    sa_Haelia = 1
    sa_Goria = 2
    sa_Gravia = 3
    sa_Baune = 4
    sa_Adonai = 5
    sa_Sila = 6

    def __str__(self):
        return self.name.replace('_', ' ')


class AlchemySolution(MagicItem):
    potency: Potency

    def __init__(
            self,
            name: str,
            potency: int,
            archetypes: List[Archetype] = [],
            weight=0.1,
            price=0
            ):
        super().__init__(name, archetypes, weight, price)
        self.potency = Potency(potency)

    def __str__(self):
        return self.name + ' ' + str(self.potency)

    def to_dict(self):
        d = super().to_dict()
        d.update({
            'potency': self.potency
            })
        return d

    def dilute(self) -> List[AlchemySolution]:
        if self.potency.value <= 1:
            return [self]
        else:
            mixture = AlchemySolution(
                    name=self.name,
                    archetypes=self.archetypes,
                    potency=self.potency.value - 1
                    )
            return [mixture, copy(mixture)]

    @classmethod
    def Concentrate(cls, mixtures: List[AlchemySolution]) -> List[AlchemySolution]:
        d = cls.MakeDict(mixtures)
        output = []
        for mixture in d:
            news_count = d[mixture] // 3
            olds_count = d[mixture] - 3 * news_count
            for i in range(news_count):
                output.append(AlchemySolution(
                    name=mixture.name,
                    archetypes=mixture.archetypes,
                    potency=mixture.potency.value + 1
                    ))
            for i in range(olds_count):
                output.append(copy(mixture))
        return output
