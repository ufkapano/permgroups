#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm
from permgroups.simsgroups import Group

# +-----------+
# | 1    2   3|
# | 4   Up   5|
# | 6    7   8|
# +-----------+-----------+----------+----------+
# | 9   10  11|17   18  19|25  26  27|33  34  35|
# |12 Front 13|20 Right 21|28 Back 29|36 Left 37|
# |14   15  16|22   23  24|30  31  32|38  39  40|
# +-----------+-----------+----------+----------+
# |41   42  43|
# |44  Down 45|
# |46   47   0|
# +-----------+

class TestRubikGroup3Center(unittest.TestCase):

    def setUp(self):
        self.N = 48
        self.group = Group()
        self.order_rubik3 = 43252003274489856000
        U1 = Perm()(1,3,8,6)(2,5,7,4)(9,33,25,17)(10,34,26,18)(11,35,27,19)
        L1 = Perm()(33,35,40,38)(34,37,39,36)(1,9,41,32)(4,12,44,29)(6,14,46,27)
        F1 = Perm()(9,11,16,14)(10,13,15,12)(6,17,43,40)(7,20,42,37)(8,22,41,35)
        R1 = Perm()(17,19,24,22)(18,21,23,20)(8,25,0,16)(5,28,45,13)(3,30,43,11)
        B1 = Perm()(25,27,32,30)(26,29,31,28)(3,33,46,24)(2,36,47,21)(1,38,0,19)
        D1 = Perm()(41,43,0,46)(42,45,47,44)(14,22,30,38)(15,23,31,39)(16,24,32,40)
        U2 = U1 * U1
        U3 = U1 * U2
        L2 = L1 * L1
        L3 = L1 * L2
        F2 = F1 * F1
        F3 = F1 * F2
        R2 = R1 * R1
        R3 = R1 * R2
        D2 = D1 * D1
        D3 = D1 * D2
        B2 = B1 * B1
        B3 = B1 * B2
        #self.generators = [U1, L1, F1, R1, B1, D1]
        self.generators = [U1, D1]   # order 16
        # cwiartki i polowki
        #self.face_turns = [U1, U2, U3, L1, L2, L3, F1, F2, F3, R1, R2, R3, D1, D2, D3, B1, B2, B3]
        self.face_turns = [L1, R1]   # order 16
        # tylko cwiartki
        #self.quarter_turns = [U1, U3, L1, L3, F1, F3, R1, R3, D1, D3, B1, B3]
        self.quarter_turns = [F1, B1]   # order 16

    def test_insert_generators(self):
        for perm in self.generators:
            self.group.insert(perm)
        #self.assertEqual(self.group.order(), self.order_rubik3) # time 37.261s
        self.assertEqual(self.group.order(), 16)

    def test_insert_face_turns(self):
        for perm in self.face_turns:
            self.group.insert(perm)
        #self.assertEqual(self.group.order(), self.order_rubik3) # time 36.091s
        self.assertEqual(self.group.order(), 16)

    def test_insert_quarter_turns(self):
        for perm in self.quarter_turns:
            self.group.insert(perm)
        #self.assertEqual(self.group.order(), self.order_rubik3) # time 37.520s
        self.assertEqual(self.group.order(), 16)

    def tearDown(self): pass

# +----------+
# | 1   2   3|
# | 4   5   6|
# | X   7   8|
# +----------+----------+----------+----------+
# | X   9  10|17  18  19|26  27  28|35  36   X|
# |11  12  13|20  21  22|29  30  31|37  38  39|
# |14  15  16|23  24  25|32  33  34|40  41  42|
# +----------+----------+----------+----------+
# |43  44  45|
# |46  47  48|
# |49  50   0|
# +----------+

class TestRubikGroup3Corner(unittest.TestCase):

    def setUp(self):
        self.N = 51
        self.group = Group()
        self.order_rubik3 = 43252003274489856000
        X1 = Perm()(1,40,0,19)(2,37,50,22)(3,35,49,25)(26,28,34,32)(27,31,33,29)
        X2 = Perm()(4,41,48,18)(5,38,47,21)(6,36,46,24)
        Y1 = Perm()(3,32,45,10)(6,29,48,13)(8,26,0,16)(17,19,25,23)(18,22,24,20)
        Y2 = Perm()(2,33,44,9)(5,30,47,12)(7,27,50,15)
        Z1 = Perm()(14,23,32,40)(15,24,33,41)(16,25,34,42)(43,45,0,49)(44,48,50,46)
        Z2 = Perm()(11,20,29,37)(12,21,30,38)(13,22,31,39)
        #self.generators = [X1, X2, Y1, Y2, Z1, Z2]
        #self.generators = [X1, X2]   # order 16
        #self.generators = [Y1, Y2]   # order 16
        self.generators = [Z1, Z2]   # order 16

    def test_insert_generators(self):
        for perm in self.generators:
            self.group.insert(perm)
        #self.assertEqual(self.group.order(), self.order_rubik3) # time 54.635s
        self.assertEqual(self.group.order(), 16)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
