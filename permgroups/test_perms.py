#!/usr/bin/env python3

import unittest
from permgroups.perms import Perm


class TestPerm(unittest.TestCase):

    def setUp(self):
        self.E = Perm()
        self.R1 = Perm()(0, 1)(2, 3)
        self.R2 = Perm()(0, 2)(1, 3)
        self.P1 = Perm()(1, 2)
        self.H = Perm()(0, 1, 3, 2)

    def test_init(self):
        self.assertEqual(self.P1, Perm()(*(1, 2)))
        self.assertEqual(self.P1, Perm(data=[0, 2, 1]))
        self.assertEqual(Perm(), Perm()(1)(2)) # singletony

    def test_bool(self):
        self.assertTrue(self.E)
        self.assertTrue(self.R1)

    def test_repr(self):
        self.assertEqual(repr(self.E), "Perm()")
        self.assertEqual(repr(self.R1), "Perm()(0, 1)(2, 3)")
        self.assertEqual(repr(self.R2), "Perm()(0, 2)(1, 3)")
        self.assertEqual(repr(self.P1), "Perm()(1, 2)")
        self.assertEqual(repr(self.H), "Perm()(0, 1, 3, 2)")

    def test_label(self):
        self.assertEqual(self.E.label(), "0")
        self.assertEqual(self.E.label(3), "012")
        self.assertEqual(self.R1.label(), "1032")
        self.assertEqual(self.P1.label(), "021")
        self.assertEqual(self.H.label(), "1302")

    def test_identity(self):
        self.assertTrue(self.E.is_identity())
        self.assertFalse(self.R1.is_identity())
        self.assertFalse(self.H.is_identity())

    def test_mul(self):
        self.assertEqual(self.E * self.E, self.E)
        self.assertEqual(self.R1 * self.E, self.R1)
        self.assertEqual(self.R1 * self.R1, self.E)
        self.assertNotEqual(self.R1 * self.R2, self.E)

    def test_invert(self):
        self.assertEqual(~self.E, self.E)
        self.assertEqual(~self.R1, self.R1)
        self.assertEqual(~self.R2, self.R2)
        self.assertNotEqual(~self.H, self.H)
        self.assertEqual(self.H * ~self.H, self.E)

    def test_order(self):
        self.assertEqual(self.E.order(), 1)
        self.assertEqual(self.R1.order(), 2)
        self.assertEqual(self.P1.order(), 2)
        self.assertEqual(self.H.order(), 4)

    def test_cmp(self):
        self.assertTrue(self.E == Perm(data=[0, 1, 2]))
        self.assertFalse(self.H == self.E)
        self.assertTrue(self.H != self.H * self.H)
        self.assertTrue(self.E != self.H)

    def test_parity(self):
        self.assertEqual(self.E.parity(), 0)
        self.assertEqual(self.R1.parity(), 0)
        self.assertEqual(self.P1.parity(), 1)
        self.assertEqual(self.H.parity(), 1)
        self.assertFalse(self.H.is_even())
        self.assertTrue(self.H.is_odd())
        self.assertEqual(self.H.sign(), -1)

    def test_call(self):
        self.assertEqual(Perm()(0)(2)()(1, 3), Perm()(1, 3))
        self.assertEqual(Perm()(2, 3) * Perm()(1, 2), Perm()(1, 3, 2))
        self.assertEqual(Perm()(2, 3)(1,2), Perm()(1, 3, 2))
        self.assertEqual(Perm()(1, 2) * Perm()(2, 3), Perm()(1, 2, 3))
        self.assertEqual(Perm()(1, 2)(2, 3), Perm()(1, 2, 3))

    def test_getitem(self):
        self.assertEqual(self.H[0], 1)
        self.assertEqual(self.H[1], 3)
        self.assertEqual(self.H[2], 0)
        self.assertEqual(self.H[3], 2)
        self.assertEqual(self.H[8], 8)

    def test_pow(self):
        self.assertEqual(pow(self.H,0), self.E)
        self.assertEqual(pow(self.H,1), self.H)
        self.assertEqual(pow(self.H,-1), ~self.H)
        self.assertEqual(pow(self.H,4), self.E)
        self.assertEqual(pow(self.H,3), ~self.H)

    def test_min_max(self):
        self.assertEqual(self.E.min(), 0)  # konwencja
        self.assertEqual(self.E.max(), 0)  # konwencja
        self.assertEqual(self.H.min(), 0)
        self.assertEqual(self.H.max(), 3)
        self.assertEqual(self.P1.min(), 1)
        self.assertEqual(self.P1.max(), 2)

    def test_list(self):  # domyslnie wypisuje do perm.max()
        self.assertEqual(self.E.list(), [0])
        self.assertEqual(self.E.list(4), [0, 1, 2, 3])
        self.assertEqual(self.P1.list(), [0, 2, 1])
        # assertRaises(exception, callable, ...)
        self.assertRaises(ValueError, lambda: self.H.list(2))

    def test_support(self):
        self.assertEqual(self.E.support(), [])
        self.assertEqual(set(self.R1.support()), set([0, 1, 2, 3]))
        self.assertEqual(set(self.P1.support()), set([1, 2]))
        self.assertEqual(set(self.H.support()), set([0, 1, 2, 3]))

    def test_commutator(self):
        self.assertTrue(self.E.commutes_with(self.H))
        self.assertTrue(self.R1.commutes_with(self.R2))
        self.assertNotEqual(self.H.commutator(self.R1), self.E)

    def test_lehmer(self):
        size = 4
        p = Perm()(0,3)(1,2)   # [3, 2, 1, 0]
        self.assertEqual(p.inversion_vector(size), [3, 2, 1, 0])
        self.assertEqual(self.E.rank_lex(size), 0)
        self.assertEqual(self.R1.rank_lex(size), 7)
        self.assertEqual(self.P1.rank_lex(size), 2)
        self.assertEqual(self.H.rank_lex(size), 10)
        self.assertEqual(Perm.unrank_lex(size, 17), Perm()(0, 2, 1, 3))

    def test_hash(self):
        aset = set()
        aset.add(self.E)
        aset.add(self.E)  # ignored
        self.assertEqual(len(aset), 1)
        aset.add(self.H)
        aset.add(self.H)  # ignored
        self.assertEqual(len(aset), 2)

    def tearDown(self): pass

if __name__== "__main__":

    unittest.main()

# EOF
