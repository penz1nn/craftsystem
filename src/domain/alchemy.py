from typing import List

from .item import Item
from .recipe import ProductionCondition

ALEMBIC = ProductionCondition('alembic', 'use alembic to produce')
DISSOLVE = ProductionCondition('dissolve', 'dissolve items to produce')
ALCHEMY = ProductionCondition('alchemy', 'use alchemy stand to produce')
ALCHEMIST_KIT = ProductionCondition('alch_kit', 'use alchemist kit to produce')


class AlchemyEffect:
    name: str
    descr: str
    is_harmful: bool

    def __init__(self, name: str, is_harmful=False, descr: str = ''):
        self.name = name
        self.descr = descr
        self.is_harmful = is_harmful

    def __str__(self):
        text = self.name
        if self.descr:
            text += ': ' + self.descr
        return text

    def to_dict(self):
        return {
                'name': self.name,
                'descr': self.descr,
                'is_harmful': self.is_harmful
                }

    def __eq__(self, o):
        return self.to_dict() == o.to_dict()

    def __hash__(self):
        return hash(str(self.to_dict()))


class AlchemyIngredient(Item):
    effects: List[AlchemyEffect]

    def __init__(
            self,
            name,
            effects: List[AlchemyEffect] = [],
            weight: float = 0,
            price: float = 0
            ):
        super().__init__(name, weight, price)
        self.effects = effects

    def to_dict(self):
        d = super().to_dict()
        d.update({
            'effects': self.effects
            })
        return d


class Potion(Item):
    effects: List[AlchemyEffect]
    descr: str

    def __init__(
            self,
            name: str,
            effects: List[AlchemyEffect],
            descr: str,
            weight: float = 0.5,
            price: float = 0
            ):
        super().__init__(name, weight, price)
        self.effects = effects
        self.descr = descr

    def to_dict(self):
        d = super().to_dict()
        d.update({
            'effects': self.effects,
            'descr': self.descr
            })
        return d

    def is_poison(self):
        for e in self.effects:
            if e.is_harmful:
                return True
        return False
