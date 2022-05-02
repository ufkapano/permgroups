#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
#from permgroups.groups import Group
from permgroups.setsgroups import Group


class TestAlternatingGroup(unittest.TestCase):

    def setUp(self): pass

    def test_alt_5(self):
        self.N = 5
        self.group = Group()
        self.assertEqual(self.group.order(), 1)
        self.group.insert(Perm()(0, 1, 2))
        self.assertEqual(self.group.order(), 3)
        self.group.insert(Perm()(1, 2, 3))
        self.assertEqual(self.group.order(), 12)
        self.group.insert(Perm()(2, 3, 4))
        self.assertEqual(self.group.order(), 60)
        self.assertFalse(Perm()(0, 1) in self.group)
        self.assertTrue(Perm()(*range(self.N)) in self.group) # N is odd
        self.assertTrue(self.group.is_transitive(points=range(self.N)))
        self.assertEqual(len(self.group.orbits(range(self.N))), 1)

    def test_alt_n(self):
        self.N = 5
        self.assertTrue(self.N > 2)
        self.group = Group()
        order = 1
        for i in range(self.N-2):
            self.group.insert(Perm()(i, i+1, i+2))
            order = order * (i+3)
            self.assertEqual(self.group.order(), order)
        self.assertTrue(self.group.is_transitive(points=range(self.N)))
        self.assertEqual(len(self.group.orbits(range(self.N))), 1)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
