#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
#from permgroups.setsgroups import Group
from permgroups.simsgroups import Group

# +-------------+
# |  1  2  3  4 |
# |  5  6  7  8 |
# |  9 10 11 12 |
# |  X 13 14 15 |
# +-------------+-------------+-------------+-------------+
# |  X 16 17 18 | 31 32 33 34 | 47 48 49 50 | 63 64 65  X |
# | 19 20 21 22 | 35 36 37 38 | 51 52 53 54 | 66 67 68 69 |
# | 23 24 25 26 | 39 40 41 42 | 55 56 57 58 | 70 71 72 73 |
# | 27 28 29 30 | 43 44 45 46 | 59 60 61 62 | 74 75 76 77 |
# +-------------+-------------+-------------+-------------+
# | 78 79 80 81 |
# | 82 83 84 85 |
# | 86 87 88 89 |
# | 90 91 92  0 |
# +-------------+

class TestRubikGroup4Corner(unittest.TestCase):

    def setUp(self):
        self.N = 93
        self.group = Group()
        self.order_rubik4 = 707195371192426622240452051915172831683411968000000000
        X1 = Perm()(1,74,0,34)(2,70,92,38)(3,66,91,42)\
            (4,63,90,46)(47,50,62,59)(48,54,61,55)(49,58,60,51)(52,53,57,56)
        X2 = Perm()(5,75,89,33)(6,71,88,37)(7,67,87,41)(8,64,86,45)
        X3 = Perm()(9,76,85,32)(10,72,84,36)(11,68,83,40)(12,65,82,44)
        Y1 = Perm()(4,59,81,18)(8,55,85,22)(12,51,89,26)\
            (15,47,0,30)(31,34,46,43)(32,38,45,39)(33,42,44,35)(36,37,41,40)
        Y2 = Perm()(3,60,80,17)(7,56,84,21)(11,52,88,25)(14,48,92,29)
        Y3 = Perm()(2,61,79,16)(6,57,83,20)(10,53,87,24)(13,49,91,28)
        Z1 = Perm()(27,43,59,74)(28,44,60,75)(29,45,61,76)\
            (30,46,62,77)(78,81,0,90)(79,85,92,86)(80,89,91,82)(83,84,88,87)
        Z2 = Perm()(23,39,55,70)(24,40,56,71)(25,41,57,72)(26,42,58,73)
        Z3 = Perm()(19,35,51,66)(20,36,52,67)(21,37,53,68)(22,38,54,69)
        #self.generators = [X1, X2, X3, Y1, Y2, Y3, Z1, Z2, Z3]
        self.generators = [X1, X2, X3]   # order 64
        #self.generators = [Y1, Y2, Y3]   # order 64
        #self.generators = [Z1, Z2, Z3]   # order 64

    def test_insert_generators(self):
        for perm in self.generators:
            self.group.insert(perm)
        #self.assertEqual(self.group.order(), self.order_rubik4)
        self.assertEqual(self.group.order(), 64)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
