#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
#from permgroups.groups import Group
from permgroups.setsgroups import Group


class TestDihedralGroup(unittest.TestCase):

    def setUp(self):
        self.N = 6
        self.assertTrue(self.N > 2)
        self.group = Group()
        self.H = Perm()(*range(self.N))
        self.group.insert(self.H)
        left = 1
        right = self.N - 1
        perm = Perm()
        while left < right:
            perm = perm * Perm()(left, right)
            left = left + 1
            right = right - 1
        self.group.insert(perm)

    def test_insert(self):
        self.assertEqual(self.group.order(), 2 * self.N)
        self.assertTrue(Perm() in self.group)
        self.assertTrue(self.H in self.group)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
