#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
from permgroups.simsgroups import Group


class TestGroup(unittest.TestCase):

    def setUp(self):
        self.N = 4
        self.G = Group()
        # Dodajemy dwa obroty.
        self.E = Perm()
        self.R1 = Perm()(0,1)(2,3)
        self.R2 = Perm()(0,2)(1,3)
        self.G.insert(self.R1)
        self.G.insert(self.R2)

    def test_group(self):
        self.assertEqual(self.G.order(), 4)
        self.assertTrue(self.E in self.G)
        self.assertFalse(Perm()(0,1) in self.G)
        self.assertEqual(set(self.G.iterperms()),
        set([Perm()(0, 1)(2, 3), Perm(), Perm()(0, 3)(1, 2), Perm()(0, 2)(1, 3)]))

    def test_is_trivial(self):
        self.assertTrue(Group().is_trivial())
        self.assertFalse(self.G.is_trivial())

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()     # run tests

# EOF
