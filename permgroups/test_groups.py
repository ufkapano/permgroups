#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
from permgroups.groups import Group


class TestGroupOrbits(unittest.TestCase):

    def setUp(self): pass

    def test_orbits1(self):
        self.N = 3
        self.group = Group()
        self.group.insert(Perm()(0,1))
        self.assertEqual(self.group.orbits(range(self.N)), [[0, 1],[2]])
        self.assertEqual(self.group.orbits([0, 1]), [[0, 1]])
        self.assertFalse(self.group.is_transitive(points=range(self.N)))
        self.assertTrue(self.group.is_transitive(points=range(self.N), strict=False))

    def test_orbits2(self):
        self.N = 4
        self.group = Group()
        self.group.insert(Perm()(0, 1))
        self.group.insert(Perm()(2, 3))
        self.assertFalse(self.group.is_transitive(points=range(self.N)))
        self.assertEqual(self.group.orbits(range(self.N)), [[0, 1],[2, 3]])
        self.assertEqual(self.group.orbits([0, 1]), [[0, 1]])
        self.assertEqual(self.group.orbits([0, 1, 2]), [[0, 1],[2, 3]])

    def test_orbits3(self):  # grupa cykliczna
        self.N = 10
        self.group = Group()
        self.group.insert(Perm()(*range(self.N)))
        self.assertTrue(self.group.is_transitive(points=range(self.N)))

    def test_orbits4(self):
        self.N = 10
        self.group = Group()
        self.group.insert(Perm()(0, 1, 2))
        self.assertFalse(self.group.is_transitive(points=range(self.N)))
        self.assertTrue(self.group.is_transitive(strict=False, points=range(self.N)))

    def tearDown(self): pass


class TestSubgroup(unittest.TestCase):

    def setUp(self):
        self.N = 4
        # Make symmetric group S_N.
        self.group1 = Group()
        self.group1.insert(Perm()(0, 1))
        self.group1.insert(Perm()(*range(self.N)))

    def test_subgroup_search(self):
        self.assertEqual(self.group1.order(), 24)
        # Dopuszczam permutacje parzyste - grupa alternujaca A_N.
        self.group2 = self.group1.subgroup_search(lambda x: x.is_even())
        self.assertEqual(self.group2.order(), 12)
        self.assertTrue(self.group2.is_transitive(points=range(self.N)))
        #print self.group2

    def test_stabilizer(self):
        self.group2 = self.group1.stabilizer(3)
        self.assertEqual(self.group2.order(), 6)
        #print self.group2

    def test_centralizer(self):
        # Tworze grupe cykliczna.
        self.group2 = Group()
        self.group2.insert(Perm()(*range(self.N)))
        self.assertEqual(self.group2.order(), self.N)
        # centrum grupy abelowej cyklicznej to cala grupa
        self.group3 = self.group2.center()
        self.assertEqual(self.group3.order(), self.N)
        # Dalej dla grupy symetrycznej.
        self.group2 = self.group1.center()
        self.assertEqual(self.group2.order(), 1)

    def test_normalizer(self):
        pass

    def test_normal_closure(self):
        n = 5
        # Tworze grupe cykliczna C_5.
        C5 = Group()
        C5.insert(Perm()(*range(n)))
        self.assertEqual(C5.order(), n)
        # Make Sym(5).
        S5 = Group()
        S5.insert(Perm()(*range(n)))
        S5.insert(Perm()(0, 1))
        self.assertEqual(S5.order(), 120)
        A5 = S5.normal_closure(C5)
        self.assertEqual(A5.order(), 60)
        for perm in A5.iterperms():
            self.assertTrue(perm.is_even())

    def test_derived_subgroup(self):
        pass

    def test_is_subgroup(self):
        self.group2 = Group()
        # Make cyclic group C_N.
        self.group2.insert(Perm()(*range(self.N)))
        self.assertEqual(self.group2.order(), self.N)
        self.assertTrue(self.group2.is_subgroup(self.group1))
        self.assertTrue(self.group2.is_abelian())
        self.assertFalse(self.group1.is_abelian())
        self.assertFalse(self.group2.is_normal(self.group1))

    def test_is_normal(self):
        a = Perm()(0, 1, 2)
        b = Perm()(0, 1)
        c = Perm()(0, 2, 1)
        G = Group()
        G.insert(a)
        G.insert(b)
        self.assertEqual(G.order(), 6)   # G = S_3
        H = Group()
        H.insert(a)
        H.insert(c)
        self.assertEqual(H.order(), 3)   # H = A_3
        self.assertTrue(H.is_normal(G))

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()     # run tests

# EOF
