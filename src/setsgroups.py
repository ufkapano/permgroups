#!/usr/bin/python

from perms import Perm


class Group(set):
    """The class defining a perm group."""

    def __init__(self):
        """Load up a Group instance."""
        self.add(Perm())

    # __str__ dziedziczone z set

    order = set.__len__            # the group order

    def insert(self, perm):
        """The perm inserted into the group generates new 
        perms in order to satisfy the group properties."""
        if perm in self:
            return
        old_order = len(self)
        self.add(perm)
        perms_added = set([perm])
        perms_generated = set()
        new_order = len(self)
        while new_order > old_order:
            old_order = new_order
            for perm1 in perms_added:
                for perm2 in self:
                    perm3 = perm1 * perm2
                    if perm3 not in self:
                        perms_generated.add(perm3)
            self.update(perms_generated)
            perms_added = perms_generated
            perms_generated = set()
            new_order = len(self)

    # __contains__ dziedziczone z set

    def listperms(self):
        """Return the list of perms."""
        return list(self)

    def iterperms(self):
        """The generator for perms from the group."""
        return iter(self)

    def is_trivial(self):
        """Test if the group is trivial."""
        return len(self) == 1

    def orbits(self, points):
        """Return a list of orbits."""
        used = set()
        orblist = list()
        for pt1 in points:
            if pt1 in used:
                continue
            orb = [pt1]     # we start a new orbit
            used.add(pt1)
            for perm in self:
                pt2 = perm[pt1]
                if pt2 not in used:
                    orb.append(pt2)
                    used.add(pt2)
            orblist.append(orb)
        return orblist

    def is_transitive(self, points, strict=True):
        """Test if the group is transitive (has a single orbit).
        If strict is False the group is transitive if it has 
        a single orbit of length different from 1.
        """
        # Jest problem, bo nie ma self.size dla grupy.
        if strict:
            return len(self.orbits(points)) == 1
        else:   # ignorujemy nieruchome punkty
            number = sum(1 for orb in self.orbits(points) if len(orb) > 1)
            return number == 1

    def subgroup_search(self, prop):
        """Return a subgroup of all elements satisfying the property."""
        # Jezeli prop(perm) jest True, to perm zaliczamy do podgrupy.
        # Funkcja prop() nie moze byc byle jaka.
        new_group = Group()
        for perm in self:
            if prop(perm):
                new_group.insert(perm)
        return new_group

    def stabilizer(self, point):
        """Return a stabilizer subgroup."""
        new_group = Group()
        for perm in self:
            if perm[point] == point:
                new_group.insert(perm)
        return new_group

    def centralizer(self, other):
        """G.centralizer(H) - return the centralizer of H."""
        if other.is_trivial() or self.is_trivial():
            return self
        new_group = Group()
        for perm1 in self:
            if all(perm1 * perm2 == perm2 * perm1 for perm2 in other):
                new_group.insert(perm1)
        return new_group

    def center(self):
        """Return the center of the group."""
        return self.centralizer(self)

    def normalizer(self, other):
        """G.normalizer(H) - return the normalizer of H."""
        new_group = Group()
        for perm1 in self:
            if all((perm1 * perm2 * ~perm1 in other) for perm2 in other):
                new_group.insert(perm1)
        return new_group

    def is_abelian(self):
        """Test if the group is abelian."""
        for perm1 in self:
            for perm2 in self:
                # Trzeba umiec porownywac perms.
                #if perm2 <= perm1:
                    #continue
                if not perm1.commutes_with(perm2):
                    return False
        return True

    def is_subgroup(self, other):
        """G1.is_subgroup(G2) - test if G1 is a subgroup of G2.
        Return True if all elements of G1 belong to G2.
        """
        if other.order() % self.order() != 0:
            return False
        return all(perm in other for perm in self)

    def is_normal(self, other):
        """G1.is_normal(G2) - test if G1 is a normal subgroup of G2.
        For each g1 in G1, g2 in G2, g2*g1*~g2 belongs to G.
        """
        for perm1 in self:
            for perm2 in other:
                if perm2 * perm1 * ~perm2 not in self:
                    return False
        return True

    def commutator(self, group1, group2):
        """Return the commutator of the groups."""
        new_group = Group()
        for perm1 in group1:
            for perm2 in group2:
                new_group.insert(perm1.commutator(perm2))
        return new_group

    def derived_subgroup(self):
        """Return the derived subgroup of the group."""
        return self.commutator(self, self)

    def action(self, points):
        """Return a new group induced by the action."""
        # Sprawdzamy, czy grupa jest tranzytywna na punktach.
        if not self.is_transitive(points):
            raise TypeError("the group is not transitive on points")
        adict = dict()
        for i, pt in enumerate(points):
            adict[pt] = i
        new_group = Group()
        for perm in self:
            new_data = [adict[perm[pt]] for pt in points]
            new_group.insert(Perm(data=new_data))
        return new_group

# EOF
