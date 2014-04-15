#!/usr/bin/python
#
# groups.py
#

from perms import Perm

class Group(dict):
    """The class defining a perm group."""

    def __init__(self):
        """Loads up a Group instance."""
        perm = Perm()
        self[perm.label()] = perm

    # __str__ dziedziczone z dict

    order = dict.__len__            # the group order

    def insert(self, perm):
        """The perm inserted into the group generates new 
        perms in order to satisfy the group properties."""
        label1 = perm.label()
        if perm in self:
            return
        old_order = self.order()
        self[label1] = perm
        perms_added = {}
        perms_added[label1] = perm
        perms_generated = {}
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
            perms_generated = {}
            new_order = self.order()

    def __contains__(self, perm):   # perm in group
        """ Test if the perm belongs to the group."""
        return dict.__contains__(self, perm.label())

    def listperms(self):
        """Returns the list of perms."""
        return self.values()

    def iterperms(self):            # generator
        """The generator for perms from the group."""
        return self.itervalues()

    def listlabels(self):
        """Returns a list of labels."""
        return self.keys()

    def iterlabels(self):
        """The generator for perm labels from the group."""
        return self.iterkeys()

    def is_trivial(self):
        """Test if the group is trivial."""
        return self.order() == 1

    def orbits(self, points):
        """Returns a list of orbits."""
        used = {}
        orblist = []
        for pt1 in points:
            if pt1 in used:
                continue
            orb = [pt1]     # we start a new orbit
            used[pt1] = True
            for perm in self.iterperms():
                pt2 = perm[pt1]
                if pt2 not in used:
                    orb.append(pt2)
                    used[pt2] = True
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
            tmp = sum(1 for orb in self.orbits(points) if len(orb) > 1)
            return tmp == 1

    def subgroup_search(self, prop):
        """Returns a subgroup of all elements satisfying the property."""
        # Jezeli prop(perm) jest True, to perm zaliczamy do podgrupy.
        # Funkcja prop() nie moze byc byle jaka.
        newgroup = Group()
        for perm in self.iterperms():
            if prop(perm):
                newgroup.insert(perm)
        return newgroup

    def stabilizer(self, point):
        """Returns a stabilizer subgroup."""
        newgroup = Group()
        for perm in self.iterperms():
            if perm[point] == point:
                newgroup.insert(perm)
        return newgroup

    def centralizer(self, other):
        """G.centralizer(H) - returns the centralizer of H."""
        if other.is_trivial() or self.is_trivial():
            return self
        newgroup = Group()
        for perm1 in self.iterperms():
            if all(perm1 * perm2 == perm2 * perm1 
            for perm2 in other.iterperms()):
                newgroup.insert(perm1)
        return newgroup

    def center(self):
        """Returns the center of the group."""
        return self.centralizer(self)

    def normalizer(self, other):
        """G.normalizer(H) - returns the normalizer of H."""
        newgroup = Group()
        for perm1 in self.iterperms():
            if all((perm1 * perm2 * ~perm1 in other) 
            for perm2 in other.iterperms()):
                newgroup.insert(perm1)
        return newgroup

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
        """G1.is_subgroup(G2)
        Test if G1 is a subgroup of G2.
        Return True if all elements of G1 belong to G2.
        """
        if other.order() % self.order() != 0:
            return False
        return all(perm in other for perm in self.iterperms())

    def is_normal(self, other):
        """G1.is_normal(G2)
        Test if G1 is a normal subgroup of G2.
        For each g1 in G1, g2 in G2, g2*g1*~g2 belongs to G.
        """
        for perm1 in self.iterperms():
            for perm2 in other.iterperms():
                if perm2 * perm1 * ~perm2 not in self:
                    return False
        return True

    def commutator(self, group1, group2):
        """Returns the commutator of the groups."""
        newgroup = Group()
        for perm1 in group1.iterperms():
            for perm2 in group2.iterperms():
                newgroup.insert(perm1.commutator(perm2))
        return newgroup

    def derived_subgroup(self):
        """Returns the derived subgroup of the group."""
        return self.commutator(self, self)

    def action(self, points):
        """Return a new group induced by the action."""
        # Sprawdzamy, czy grupa jest tranzytywna na punktach.
        if not self.is_transitive(points):
            raise TypeError("the group is not transitive on points")
        adict = {}
        for i, pt in enumerate(points):
            adict[pt] = i
        newgroup = Group()
        for perm in self.iterperms():
            newdata = [adict[perm[pt]] for pt in points]
            newgroup.insert(Perm(data=newdata))
        return newgroup

if __name__== "__main__":

    pass

# EOF
