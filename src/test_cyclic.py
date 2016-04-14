#!/usr/bin/python

import unittest
from perms import Perm
#from groups import Group
from setsgroups import Group


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
        self.assertFalse(Perm()(*range(self.N)) in self.group)
        self.assertFalse(self.group.is_transitive(points=range(self.N)))
        self.assertEqual(len(self.group.orbits(range(self.N))), 2)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
