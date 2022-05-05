#!/usr/bin/env python3

try:
    integer_types = (int, long)
    range = xrange
except NameError:   # Python 3
    integer_types = (int,)

from permgroups.perms import Perm


class Group(set):
    """The class defining a perm group."""

    def __init__(self):
        """Load up a Group instance."""
        self.size = 1   # rozmiar permutacji w grupie
        # Inicjalizacja struktur.
        self.Sigma = [(k+1) * [None] for k in range(self.size)]
        # Lista Sigma[k] zawiera co najmniej identycznosc.
        for k in range(self.size):
            self.Sigma[k][k] = Perm()   # identycznosc sigma_kk
        # Silne generatory.
        self.all_Sigma = [Perm()]   # E tez dodam raz
        self.all_T = []

    def __str__(self):
        """Return a string representation of the group."""
        t = len(self.all_T)
        return "Group() with {} strong generators".format(t)

    def order(self):
        """Return the group order."""
        result = 1
        for k in range(self.size):
            result *= sum(1 for perm in self.Sigma[k] if perm)
        return result

    def __contains__(self, perm):
        """ Test if the perm belongs to the group."""
        size = perm.max() + 1
        if size > self.size:   # trzeba powiekszyc baze
            self.Sigma.extend( (k+1) * [None] for k in range(self.size, size) )
            # Lista Sigma[k] zawiera co najmniej identycznosc.
            for k in range(self.size, size):
                self.Sigma[k][k] = Perm()   # identycznosc sigma_kk
            self.size = size

        k = self.size - 1         # start od samej gory
        while k > 0:
            j = perm[k]
            if self.Sigma[k][j] is None:
                return False
            perm = ~self.Sigma[k][j] * perm
            k = k - 1
        return True

    def insert(self, perm):
        """The perm inserted into the group generates new 
        perms in order to satisfy the group properties."""
        size = perm.max() + 1
        if size > self.size:   # trzeba powiekszyc baze
            self.Sigma.extend( (k+1) * [None] for k in range(self.size, size) )
            # Lista Sigma[k] zawiera co najmniej identycznosc.
            for k in range(self.size, size):
                self.Sigma[k][k] = Perm()   # identycznosc sigma_kk
            self.size = size

        self.alg_A(perm.max(), perm)

    def alg_A(self, k, perm):
        """Append the perm to the strong generators."""
        if perm in self:
            return
        j = perm[k]
        if self.Sigma[k][j] is not None:
            perm2 = ~self.Sigma[k][j] * perm
            # Trzeba sie upewnic, jakiego rzedu jest perm.
            self.alg_A(perm2.max(), perm2)
            return
        self.all_T.append(perm)
        for item in self.all_Sigma:
            # Trzeba sie upewnic, jakiego rzedu jest perm.
            perm2 = perm * item
            self.alg_B(perm2.max(), perm2)

    def alg_B(self, k, perm):
        """Update the Sigma."""
        if perm in self:
            return
        j = perm[k]
        if self.Sigma[k][j] is None:
            self.Sigma[k][j] = perm
            self.all_Sigma.append(perm)
            for item in self.all_T:
                # Trzeba sie upewnic, jakiego rzedu jest perm.
                perm2 = item * perm
                k_max = perm2.max()
                if k_max != k:
                    self.alg_A(k_max, perm2)
                else:
                    self.alg_B(k_max, perm2)
            return
        item = ~self.Sigma[k][j] * perm
        # Trzeba sie upewnic, jakiego rzedu jest perm.
        # Tu na pewno k_max < k.
        self.alg_A(item.max(), item)

    def iterperms(self):
        """The generator for perms from the group."""
        a = [0] * self.size
        while True:
            # M2. Odwiedziny.
            if all(self.Sigma[k][a[k]] is not None for k in range(self.size)):
                perm = Perm()
                for k in range(self.size):
                    perm = self.Sigma[k][a[k]] * perm
                yield perm
            # M3. Przygotowanie do dodania jedynki.
            j = self.size - 1
            # M4. Przeniesienie, jesli trzeba.
            while a[j] == j and j >= 0:
                a[j] = 0
                j = j - 1
            # M5. Zwiekszenie, o ile nie koniec.
            if j < 0:
                break
            else:
                a[j] = a[j] + 1

    def is_trivial(self):
        """Test if the group is trivial."""
        return self.order() == 1
# EOF
