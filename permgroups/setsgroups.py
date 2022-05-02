#!/usr/bin/env python3

from permgroups.perms import Perm


class Group(set):
    """The class defining a perm group."""

    def __init__(self):
        """Load up a Group instance."""
        self.add(Perm())

    # __str__ dziedziczone z set

    order = set.__len__            # the group order

    # __contains__ dziedziczone z set

    def insert(self, perm):
        """The perm inserted into the group generates new 
        perms in order to satisfy the group properties."""
        if perm in self:
            return
        old_order = self.order()
        self.add(perm)
        perms_added = set([perm])
        perms_generated = set()
        new_order = self.order()
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
            new_order = self.order()

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
        orbit_list = list()
        for pt1 in points:
            if pt1 in used:
                continue
            orbit = [pt1]     # we start a new orbit
            used.add(pt1)
            for perm in self:
                pt2 = perm[pt1]
                if pt2 not in used:
                    orbit.append(pt2)
                    used.add(pt2)
            orbit_list.append(orbit)
        return orbit_list

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
        return self.subgroup_search(
            lambda perm: perm[point] == point)

    def centralizer(self, other):
        """G.centralizer(H) - return the centralizer of H."""
        if other.is_trivial() or self.is_trivial():
            return self
        return self.subgroup_search(lambda perm:
            all(perm * perm2 == perm2 * perm for perm2 in other))

    def center(self):
        """Return the center of the group."""
        return self.centralizer(self)

    def normalizer(self, other):
        """G.normalizer(H) - return the normalizer of H."""
        return self.subgroup_search(lambda perm:
            all((perm * perm2 * ~perm in other) for perm2 in other))

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
        """H.is_subgroup(G) - test if H is a subgroup of G.
        Return True if all elements of H belong to G.
        """
        if other.order() % self.order() != 0:
            return False
        return all(perm in other for perm in self)

    def is_normal(self, other):
        """H.is_normal(G) - test if H is a normal subgroup of G.
        For each h in H, g in G, g*h*~g belongs to H.
        """
        for perm1 in self:
            for perm2 in other:
                if perm2 * perm1 * ~perm2 not in self:
                    return False
        return True

    def normal_closure(self, other):
        """Return the normal closure (conjugate closure)."""
        new_group = Group()
        for perm1 in self:
            for perm2 in other:
                new_group.insert(perm1 * perm2 * ~perm1)
        return new_group

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
