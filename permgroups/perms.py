#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

import random
from functools import reduce


def gcd(a, b): 
    """Compute the greatest common divisor."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Compute the least common multiple."""
    return a * b // gcd(a, b)

def swap(L, i, j):
    """Exchange of two elements on the list."""
    L[i], L[j] = L[j], L[i]


class Perm(dict):
    """The class defining a perm."""

    def __init__(self, data=None):
        """Load up a Perm instance."""
        if data:
            for key, value in enumerate(data):
                self[key] = value

    def __repr__(self):
        """Compute the string representation of the perm."""
        words = ["Perm()"]
        for cycle in self.cycles():
            words.append(str(tuple(cycle)))
        return "".join(words)

    def __nonzero__(self):   # Py2
        """Return always True so Perm() is True."""
        return True

    __bool__ = __nonzero__   # Py3

    def __missing__(self, key):
        """Enter the key into the dict and return the key."""
        self[key] = key
        return key

    def __mul__(self, other):
        """Return the product of the perms."""
        perm = Perm()
        # Ustalam potrzebne klucze.
        # Najpierw other, bo self dostanie nowe klucze.
        for key in other:
            perm[key] = self[other[key]]
        # Tutaj other urosnie, ale chyba to nie szkodzi.
        for key in self:
            perm[key] = self[other[key]]
        return perm

    def label(self, size=None):
        """Return the string label for the perm."""
        if size is None:
            size = self.max() + 1
        #letters = "0123456789abcdefghijklmnopqrstuvwxyz"
        letters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
        chars = list()
        for key in range(size):
            chars.append(letters[self[key]])
        return "".join(chars)

    def max(self):
        """Return the highest element moved by the perm."""
        # Tutaj chyba dwa razy przebiegamy self.
        if self.is_identity():
            return 0
        else:
            return max(key for key in self if key != self[key])

    def min(self):
        """Return the lowest element moved by the perm."""
        # Tutaj chyba dwa razy przebiegamy self.
        # Dziala tak jak metoda dla implementacji z listami.
        if self.is_identity():
            return 0
        else:
            return min(key for key in self if key != self[key])

    def is_identity(self):
        """Test if the perm is the identity perm."""
        # Musze dopuscic sytuacje self[key] == key.
        # Tu jest cos podobnego, jak przy wielomianach.
        return all(self[key] == key for key in self)

    def __invert__(self):   # ~perm
        """Find the inverse of the perm."""
        perm = Perm()
        for key in self:
            perm[self[key]] = key
        return perm

    def __call__(self, *args):          # perm(a, b, ...)
        """Return the product of the perm and the cycle."""
        changed = dict()
        n = len(args)
        # Trzeba przemnozyc po mojemu self * other.
        # Musze wykorzystac tymczasowy slownik.
        for i in range(n):
            changed[args[i]] = self[args[(i + 1) % n]]
        self.update(changed)
        return self

    def __getitem__(self, key):          # perm[k]
        """Find the item on the given position."""
        return dict.__getitem__(self, key)

    def order(self):
        """Return the order of the perm."""
        alist = [len(cycle) for cycle in self.cycles()]
        return reduce(lcm, alist, 1)

    def __eq__(self, other):
        """Test if the perms are equal."""
        return (self * ~other).is_identity()

    def __ne__(self, other):
        """Test if the perms are not equal."""
        return not self == other

    def __pow__(self, n):
        """Find powers of the perm."""
        if n == 0:
            return Perm()
        if n < 0:
            return pow(~self, -n)
        perm = self
        if n == 1:
            return self
        elif n == 2:
            return self * self
        else:   # binary exponentiation
            result = Perm()  # identity
            while True:
                if n % 2 == 1:
                    result = result * perm
                    n = n - 1  # przez ile pomnozyc
                    if n == 0:
                        break
                if n % 2 == 0:
                    perm = perm * perm
                    n = n // 2  # zmienilo sie perm!
                    #print "n =", n
        return result

    def list(self, size=None):
        """Return the perm in array form."""
        if size is None:
            #size = self.size     # tu sa dwie koncepcje
            size = self.max() + 1
        elif size < self.max() + 1:
            raise ValueError("size is too small")
        return [self[key] for key in range(size)]

    def cycles(self):
        """Return a list of cycles for the perm."""
        size = self.max() + 1
        unchecked = [True] * size
        cyclic_form = list()
        for i in range(size):
            if unchecked[i]:
                cycle = list()
                cycle.append(i)
                unchecked[i] = False
                j = i
                while unchecked[self[j]]:
                    j = self[j]
                    cycle.append(j)
                    unchecked[j] = False
                if len(cycle) > 1:
                    cyclic_form.append(cycle)
        return cyclic_form

    def parity(self):
        """Return the parity of the perm (0 or 1)."""
        size = self.max() + 1
        unchecked = [True] * size
        c = 0    # liczba cykli w perm, lacznie z jednoelementowymi
        for j in range(size):
            if unchecked[j]:
                c = c + 1
                unchecked[j] = False
                i = j
                while self[i] != j:
                    i = self[i]
                    unchecked[i] = False
        return (size - c) % 2

    def is_even(self):
        """Test if the perm is even."""
        return self.parity() == 0

    def is_odd(self):
        """Test if the perm is odd."""
        return self.parity() == 1

    def sign(self):
        """Return the sign of the perm (+1 or -1)."""
        return (1 if self.parity() == 0 else -1)

    def support(self):
        """Return the elements in permutation, P, for which P[i] != i."""
        return [key for key in self if self[key] != key]

    def commutes_with(self, other):
        """Test if the perms commute."""
        # Chyba troche silowe rozwiazanie. Czy jest wolniejsze?
        return self * other == other * self

    def commutator(self, other):
        """Find the commutator of the perms."""
        return self * other * ~self * ~other

    @classmethod
    def random(cls, size):
        """Return a random perm of the given size."""
        # Usage: Perm.random(size)
        new_data = list(range(size))
        random.shuffle(new_data)
        return cls(data=new_data)

    def inversion_vector(self, size):
        """Return the inversion vector of the perm."""
        lehmer = [0] * size
        for i in range(size):
            counter = 0
            for j in range(i + 1, size):
                if self[i] > self[j]:
                    counter += 1
            lehmer[i] = counter
        return lehmer

    def rank_lex(self, size):
        """Return the lexicographic rank of the perm."""
        lehmer = self.inversion_vector(size) # zapis w systemie silniowym
        lehmer.reverse()   # trzeba odwrocic kolejnosc
        k = size - 1
        result = lehmer[k]
        while k > 0:   # zmodyfikowany horner
            k = k - 1
            result = result * (k + 1) + lehmer[k]
        return result

    @classmethod
    def unrank_lex(cls, size, rank):
        """Lexicographic perm unranking."""
        # Usage: Perm.unrank_lex(size, rank)
        #alist = [0]   # bedzie dlugosc size
        # chyba wydajniej jest od razu zrobic dobra dlugosc
        alist = [0] * size   # bedzie dlugosc size
        i = 1
        while i < size:
            i = i + 1
            #alist.append(rank%i)
            alist[i - 1] = rank % i
            rank = rank // i
        if rank > 0:
            raise ValueError("size is too small")
        alist.reverse() # to jest inversion vector
        E = list(range(size))
        new_data = list()
        # chyba pop(item) nie jest wydajne, bo jest przebudowa listy
        for item in alist:
            new_data.append(E.pop(item))
        # tutaj E jest juz puste
        assert len(E) == 0
        return cls(data=new_data)

    def rank_mr(self, size):
        """Myrvold and Ruskey rank of the perm."""
        alist = self.list(size)
        blist = (~self).list(size)
        return Perm._mr_helper(size, alist, blist)

    @classmethod
    def _mr_helper(cls, size, alist, blist):
        """A helper function for MR ranking."""
        # both alist and blist are modified
        if size == 1:
            return 0
        s = alist[size - 1]
        swap(alist, size - 1, blist[size-1])
        swap(blist, s, size - 1)
        return s + size * cls._mr_helper(size - 1, alist, blist)

    @classmethod
    def unrank_mr(cls, size, rank):
        """Myrvold and Ruskey perm unranking."""
        new_data = list(range(size))
        while size > 0:
            swap(new_data, size - 1, rank % size)
            rank = rank // size
            size = size - 1
        return cls(data=new_data)

    def __hash__(self):
        """Hashable perms."""
        return hash(tuple(self.list()))

# EOF
