#!/usr/bin/env python3
#
# Symmetries of the sudoku board 4x4.

import unittest
from permgroups.perms import Perm
#from permgroups.groups import Group
#from permgroups.setsgroups import Group
from permgroups.simsgroups import Group

# +-----+-----+
# | 1  2| 3  4|
# | 5  6| 7  8|
# +-----+-----+
# | 9 10|11 12|
# |13 14|15  0|
# +-----+-----+

class TestSudoku4x4(unittest.TestCase):

    def setUp(self):
        self.N = 16
        self.group = Group()
        self.generators = []
        self.generators.append(
            Perm()(1,2)(5,6)(9,10)(13,14))
        self.generators.append(
            Perm()(3,4)(7,8)(11,12)(15,0))
        self.generators.append(
            Perm()(1,3)(2,4)(5,7)(6,8)(9,11)(10,12)(13,15)(14,0))
        self.generators.append(
            Perm()(1,5)(2,6)(3,7)(4,8))
        self.generators.append(
            Perm()(9,13)(10,14)(11,15)(12,0))
        self.generators.append(
            Perm()(1,9)(2,10)(3,11)(4,12)(5,13)(6,14)(7,15)(8,0))
        self.generators.append(
            Perm()(1,4,0,13)(2,8,15,9)(3,12,14,5)(6,7,11,10))

    def test_insert(self):
        for perm in self.generators:
            self.group.insert(perm)
        self.assertEqual(self.group.order(), 128)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
