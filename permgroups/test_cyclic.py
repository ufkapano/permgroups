#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
#from permgroups.groups import Group
from permgroups.setsgroups import Group


class TestCyclicGroup(unittest.TestCase):

    def setUp(self):
        # The cyclic group from the paper by Knuth.
        self.N = 6
        self.H = Perm()(0, 1, 2, 4)(3, 5)
        self.group = Group()
        self.group.insert(self.H)

    def test_group(self):
        self.assertEqual(self.group.order(), 4)
        self.assertFalse(self.group.is_trivial())
        self.assertTrue(Perm() in self.group)
        self.assertTrue(self.H in self.group)
        points = range(self.N)
        self.assertFalse(Perm()(*points) in self.group)
        self.assertEqual(self.group.orbits(points), [[0, 4, 2, 1], [3, 5]])
        self.assertEqual(len(self.group.orbits(points)), 2)
        self.assertFalse(self.group.is_transitive(points))

    def test_cyclic6(self):
        points = range(5)
        C6 = Group()
        C6.insert(Perm()(0, 1, 2)(3, 4))
        self.assertEqual(C6.order(), 6)
        self.assertEqual(C6.orbits(points), [[0, 2, 1], [3, 4]])
        self.assertEqual(len(C6.orbits(points)), 2)
        self.assertFalse(C6.is_transitive(points))

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
