import unittest

from .alchemy_solutions import AlchemySolution, Archetype

a1 = Archetype('Magicka')
a2 = Archetype('Shields')


class TestAlchemySolution(unittest.TestCase):

    def setUp(self):
        self.as1 = AlchemySolution(
                name='Agea',
                archetypes=[a1],
                potency=3
                )
        self.as2 = AlchemySolution(
                name='Arden',
                archetypes=[a2],
                potency=1
                )

    def test_eq(self):
        a = AlchemySolution('Agea', 3, [a1])
        self.assertEqual(a, self.as1)
        self.assertNotEqual(self.as1, self.as2)

    def test_MakeDict(self):
        d = {}
        d[self.as2] = 2
        d[self.as1] = 1
        self.assertEqual(
                d,
                AlchemySolution.MakeDict([self.as1, self.as2, self.as2])
                )

    def test_str(self):
        self.assertEqual(
                str(self.as1),
                'Agea sa Gravia'
                )

    def test_dilute(self):
        mixtures = self.as1.dilute()
        a = AlchemySolution('Agea', 2, [a1])
        self.assertEqual(mixtures, [a, a])
        self.assertEqual([self.as2], self.as2.dilute())

    def test_Concentrate(self):
        mixtures = [self.as2] * 4
        mixtures = AlchemySolution.Concentrate(mixtures)
        a = AlchemySolution('Arden', 2, [a2])
        self.assertEqual(
                AlchemySolution.MakeDict(mixtures),
                AlchemySolution.MakeDict([a, self.as2])
                )
        mixtures.extend([a, a, self.as2, self.as2])
        as3 = AlchemySolution('Arden', 3, [a2])
        mixtures = AlchemySolution.Concentrate(mixtures)
        self.assertEqual(
                AlchemySolution.MakeDict(mixtures),
                AlchemySolution.MakeDict([as3, a])
                )
