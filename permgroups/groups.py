#!/usr/bin/env python3

from permgroups.perms import Perm


class Group(dict):
    """The class defining a perm group."""

    def __init__(self):
        """Load up a Group instance."""
        perm = Perm()
        self[perm.label()] = perm

    # __str__ dziedziczone z dict

    order = dict.__len__            # the group order

    def insert(self, perm):
        """The perm inserted into the group generates new 
        perms in order to satisfy the group properties."""
        if perm in self:
            return
        old_order = self.order()
        label1 = perm.label()
        self[label1] = perm
        perms_added = dict()
        perms_added[label1] = perm
        perms_generated = dict()
        new_order = self.order()
        while new_order > old_order:
            old_order = new_order
            for label1 in perms_added:
                for label2 in self.iterlabels():
                    perm3 = perms_added[label1] * self[label2]
                    label3 = perm3.label()
                    if perm3 not in self:
                        perms_generated[label3] = perm3
            self.update(perms_generated)
            perms_added = perms_generated
            perms_generated = dict()
            new_order = self.order()

    def __contains__(self, perm):   # perm in group
        """ Test if the perm belongs to the group."""
        return dict.__contains__(self, perm.label())

    def iterperms(self):
        """The generator for perms from the group."""
        for key in self:
            yield self[key]

    def iterlabels(self):
        """The generator for perm labels from the group."""
        for key in self:
            yield key

    def is_trivial(self):
        """Test if the group is trivial."""
        return self.order() == 1

    def orbits(self, points):
        """Return a list of orbits."""
        used = dict()   # set can be used
        orbit_list = list()
        for pt1 in points:
            if pt1 in used:
                continue
            orbit = [pt1]     # we start a new orbit
            used[pt1] = True
            for perm in self.iterperms():
                pt2 = perm[pt1]
                if pt2 not in used:
                    orbit.append(pt2)
                    used[pt2] = True
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
            number = sum(1 for orbit in self.orbits(points) if len(orbit) > 1)
            return number == 1

    def subgroup_search(self, prop):
        """Return a subgroup of all elements satisfying the property."""
        # Jezeli prop(perm) jest True, to perm zaliczamy do podgrupy.
        # Funkcja prop() nie moze byc byle jaka.
        new_group = Group()
        for perm in self.iterperms():
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
            all(perm * perm2 == perm2 * perm for perm2 in other.iterperms()))

    def center(self):
        """Return the center of the group."""
        return self.centralizer(self)

    def normalizer(self, other):
        """G.normalizer(H) - return the normalizer of H."""
        return self.subgroup_search(lambda perm:
            all((perm * perm2 * ~perm in other) for perm2 in other.iterperms()))

    def is_abelian(self):
        """Test if the group is abelian."""
        for perm1 in self.iterperms():
            for perm2 in self.iterperms():
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
        return all(perm in other for perm in self.iterperms())

    def is_normal(self, other):
        """H.is_normal(G) - test if H is a normal subgroup of G.
        For each h in H, g in G, g*h*~g belongs to H.
        """
        for perm1 in self.iterperms():
            for perm2 in other.iterperms():
                if perm2 * perm1 * ~perm2 not in self:
                    return False
        return True

    def normal_closure(self, other):
        """Return the normal closure (conjugate closure)."""
        new_group = Group()
        for perm1 in self.iterperms():
            for perm2 in other.iterperms():
                new_group.insert(perm1 * perm2 * ~perm1)
        return new_group

    def commutator(self, group1, group2):
        """Return the commutator of the groups."""
        new_group = Group()
        for perm1 in group1.iterperms():
            for perm2 in group2.iterperms():
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
        adict = dict()   # for numbering of points
        for i, pt in enumerate(points):
            adict[pt] = i
        new_group = Group()
        for perm in self.iterperms():
            new_data = [adict[perm[pt]] for pt in points]
            new_group.insert(Perm(data=new_data))
        return new_group

# EOF
