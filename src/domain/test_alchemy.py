import unittest

from .alchemy import AlchemyEffect, AlchemyIngredient, Potion


ae1 = AlchemyEffect('Restore Health')
ae2 = AlchemyEffect('Damage Magicka', is_harmful=True, descr='Harm Magicka')


class TestAlchemyEffect(unittest.TestCase):

    def test_eq(self):
        self.assertEqual(ae1, AlchemyEffect('Restore Health'))
        self.assertNotEqual(ae1, ae2)
        self.assertNotEqual(AlchemyEffect('Damage Magicka'), ae2)

    def test_hashable(self):
        d = {
                ae1: 1,
                ae2: 2
                }
        self.assertEqual(d[AlchemyEffect('Restore Health')], 1)


class TestAlchemyIngredient(unittest.TestCase):
    def setUp(self):
        self.ai1 = AlchemyIngredient(
                name="Giant's toe",
                effects=[ae1],
                )
        self.ai2 = AlchemyIngredient(
                name='Blisterwort',
                effects=[ae1, ae2]
                )

    def test_eq(self):
        self.assertEqual(self.ai1, AlchemyIngredient("Giant's toe", [AlchemyEffect('Restore Health')]))
        ai = AlchemyIngredient("Gian's toe", [ae1, ae2])
        self.assertNotEqual(self.ai1, ai)

    def test_MakeDict(self):
        d = {}
        d[self.ai1] = 2
        d[self.ai2] = 1
        self.assertEqual(d, AlchemyIngredient.MakeDict([self.ai1, self.ai1, self.ai2]))


class TestPotion(unittest.TestCase):

    def setUp(self):
        self.p1 = Potion(
                name='Healing potion',
                effects=[ae1],
                descr='Heal 10 HP'
                )
        self.p2 = Potion(
                name='Mage Poison (Crude)',
                effects=[ae1, ae2],
                descr='Damage 20 MP, Heal 10 HP'
                )

    def test_eq(self):
        p = Potion('Healing potion', [ae1], 'Heal 10 HP')
        self.assertEqual(p, self.p1)
        self.assertNotEqual(self.p1, self.p2)

    def test_MakeDict(self):
        d = {}
        d[self.p1] = 2
        d[self.p2] = 1
        self.assertEqual(d, Potion.MakeDict([self.p1, self.p2, self.p1]))

    def test_is_poison(self):
        self.assertTrue(self.p2.is_poison())
        self.assertFalse(self.p1.is_poison())
