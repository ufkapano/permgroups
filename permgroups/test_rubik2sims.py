#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
from permgroups.simsgroups import Group

# +-----+
# | 1  2|
# | X  3|
# +-----+-----+-----+-----+
# | X  4| 7  8|11 12|15  X|
# | 5  6| 9 10|13 14|16 17|
# +-----+-----+-----+-----+
# |18 19|
# |20  0|
# +-----+

class TestRubikGroup2Corner(unittest.TestCase):

    def setUp(self):
        self.N = 21
        self.group = Group()
        self.order_rubik2 = 3674160   # 6 * 9 * 12 * 15 * 18 * 21
        R1 = Perm()(2,13,19,4)(3,11,0,6)(7,8,10,9)
        D1 = Perm()(5,9,13,16)(6,10,14,17)(18,19,0,20)
        B1 = Perm()(1,16,0,8)(2,15,20,10)(11,12,14,13)
        R2 = R1 * R1
        R3 = R1 * R2
        D2 = D1 * D1
        D3 = D1 * D2
        B2 = B1 * B1
        B3 = B1 * B2
        self.generators = [R1, D1, B1]   # for simsgroups only
        # cwiartki i polowki
        self.face_turns = [R1, R2, R3, D1, D2, D3, B1, B2, B3]   # for simsgroups only
        # tylko cwiartki
        self.quarter_turns = [R1, R3, D1, D3, B1, B3]   # for simsgroups only

    def test_insert_generators(self):
        for perm in self.generators:
            self.group.insert(perm)
        self.assertEqual(self.group.order(), self.order_rubik2)

    def test_insert_face_turns(self):
        for perm in self.face_turns:
            self.group.insert(perm)
        self.assertEqual(self.group.order(), self.order_rubik2)

    def test_insert_quarter_turns(self):
        for perm in self.quarter_turns:
            self.group.insert(perm)
        self.assertEqual(self.group.order(), self.order_rubik2)

    def test_insert(self):
        self.assertEqual(self.group.order(), 1)
        self.group.insert(Perm()(0, 1, 2)(3, 5, 4))
        self.assertEqual(self.group.order(), 3)
        self.group.insert(Perm()(0, 3)(1, 4)(2, 5))
        self.assertEqual(self.group.order(), 6)
        self.group.insert(Perm()(0, 6)(1, 7)(2, 8))
        self.assertEqual(self.group.order(), 6 * 9)
        self.group.insert(Perm()(0, 9)(1, 10)(2, 11))
        self.assertEqual(self.group.order(), 6 * 9 * 12)
        self.group.insert(Perm()(0, 12)(1, 13)(2, 14))
        self.assertEqual(self.group.order(), 6 * 9 * 12 * 15)
        self.group.insert(Perm()(0, 15)(1, 16)(2, 17))
        self.assertEqual(self.group.order(), 6 * 9 * 12 * 15 * 18)
        self.group.insert(Perm()(0, 18)(1, 19)(2, 20))
        self.assertEqual(self.group.order(), 6 * 9 * 12 * 15 * 18 * 21)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
