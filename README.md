# permgroups package

Python implementation of permutation groups is presented. 
Two classes are introduced: *Perm* for permutations, 
*Group* for permutation groups (everal versions). 

The class *Perm* from the *perms* module
is based on Python dictionaries and utilize cycle notation. 
The methods of calculation for the perm order, parity, ranking and unranking 
are given. A random permutation generation is also shown. 

The class *Group* from the *groups* module
is very simple and it is also based on dictionaries. 
It is mainly the presentation of the permutation groups interface with 
methods for the group order, subgroups (normalizer, centralizer, center, 
stabilizer), orbits, and several tests.

The class *Group* from the *setgroups* module
is also simple and it is based on sets.

The class *Group* from the *simsgroups* module
is advanced and it is bases on the Sims theory.

The project is moved from *Google Code*.

## Download

To install an official release do

    python3 -m pip install permgroups

To get the git version do

    git clone https://github.com/ufkapano/permgroups.git

## Usage

~~~python
>>> from permgroups.perms import Perm
>>> from permgroups.groups import Group
>>> p = Perm()(0, 1, 2, 4)(3, 5)
>>> ~p
Perm()(0, 4, 2, 1)(3, 5)
>>> p.is_identity(), p.parity(), p.is_even(), p.sign()
(False, 0, True, 1)
>>> p.order(), pow(p, 4)
(4, Perm())
>>> Perm.random(10)
Perm()(0, 1, 4, 2, 7)(3, 9, 8)(5, 6)
>>> G = Group()
>>> G.insert(p)
>>> G.order()
4
>>> list(G.iterperms())
[Perm(), Perm()(0, 1, 2, 4)(3, 5), Perm()(0, 2)(1, 4), Perm()(0, 4, 2, 1)(3, 5)]
>>> Perm()(1, 4)(0, 2) in G, Perm()(0, 1, 2, 3) in G
(True, False)
>>> G.is_abelian()
True
~~~

## References

[1] A. Kapanowski, *Python for education: permutations*. 
http://arxiv.org/abs/1307.7042 [draft]

[2] A. Kapanowski, The Python Papers 9, 3 (2014). 
*Python for education: permutations*. [final version]
http://ojs.pythonpapers.org/index.php/tpp/article/view/258 

## Contributors

Andrzej Kapanowski (project leader)

Tomasz Gądek

EOF
