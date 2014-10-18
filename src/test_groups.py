#!/usr/bin/python

import unittest
from perms import Perm
from groups import Group


class TestCyclicGroup(unittest.TestCase):

    def setUp(self):
        self.H = Perm()(0, 1, 2, 4)(3, 5)
        self.group = Group()

    def test_insert(self):
        self.assertEqual(self.group.order(), 1)
        self.group.insert(self.H)
        self.assertEqual(self.group.order(), 4)
        self.assertTrue(Perm() in self.group)
        self.assertTrue(self.H in self.group)
        self.assertFalse(Perm()(0, 1, 2, 3, 4, 5) in self.group)

    def tearDown(self): pass


class TestSymmetricGroup(unittest.TestCase):

    def setUp(self):
        self.group = Group()

    # Test grupy symetrycznej.
    def test_insert(self):
        self.assertEqual(self.group.order(), 1)
        self.group.insert(Perm()(0, 1))
        self.assertEqual(self.group.order(), 2)
        self.group.insert(Perm()(1, 2))
        self.assertEqual(self.group.order(), 6)
        self.group.insert(Perm()(2, 3))
        self.assertEqual(self.group.order(), 24)
        #self.group.insert(Perm(,(3, 4)))
        #self.assertEqual(self.group.order(), 120)

    def tearDown(self): pass


class TestAlternatingGroup(unittest.TestCase):

    def setUp(self):
        self.group = Group()

    def test_insert(self):
        self.assertEqual(self.group.order(), 1)
        self.group.insert(Perm()(0, 1, 2))
        self.assertEqual(self.group.order(), 3)
        self.group.insert(Perm()(1, 2, 3))
        self.assertEqual(self.group.order(), 12)
        self.group.insert(Perm()(2, 3, 4))
        self.assertEqual(self.group.order(), 60)

    def tearDown(self): pass


class TestRubikGroup2(unittest.TestCase):

    def setUp(self):
        # N = 21
        self.group = Group()

    # Test grupy kostki Rubika.
    def test_insert(self):
        self.assertEqual(self.group.order(), 1)
        self.group.insert(Perm()(0, 1, 2)(3, 5, 4))
        self.assertEqual(self.group.order(), 3)
        self.group.insert(Perm()(0, 3)(1, 4)(2, 5))
        self.assertEqual(self.group.order(), 6)
        self.group.insert(Perm()(0, 6)(1, 7)(2, 8))
        self.assertEqual(self.group.order(), 6 * 9)
        #self.group.insert(Perm()(0, 9)(1, 10)(2, 11))
        #self.assertEqual(self.group.order(), 6 * 9 * 12)
        #self.group.insert(Perm()(0, 12)(1, 13)(2, 14))
        #self.assertEqual(self.group.order(), 6 * 9 * 12 * 15)
        #self.group.insert(Perm()(0, 15)(1, 16)(2, 17))
        #self.assertEqual(self.group.order(), 6 * 9 * 12 * 15 * 18)
        #self.group.insert(Perm()(0, 18)(1, 19)(2, 20))
        #self.assertEqual(self.group.order(), 6 * 9 * 12 * 15 * 18 * 21)

    def tearDown(self): pass


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
        # Tworze grupe symetryczna.
        self.group1 = Group()
        self.group1.insert(Perm()(0, 1))
        self.group1.insert(Perm()(*range(self.N)))

    def test_subgroup_search(self):
        self.assertEqual(self.group1.order(), 24)
        # Dopuszczam permutacje parzyste - grupa alternujaca.
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

    def test_is_subgroup(self):
        self.group2 = Group()
        # Tworze grupe cykliczna.
        self.group2.insert(Perm()(*range(self.N)))
        self.assertTrue(self.group2.is_subgroup(self.group1))
        self.assertTrue(self.group2.is_abelian())
        self.assertFalse(self.group1.is_abelian())
        self.assertFalse(self.group2.is_normal(self.group1))

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()     # run tests

# EOF
