# UFDS - Union-Find (Disjoint Set) Data Structure

Union-Find (aka Disjoint Set) Data Structure using the Forest-of-Trees
implementation.

## TL;DR

```py
# import the user facing DisjointSet class
from ufds import DisjointSet

# create a new DisjointSet instance
ds = DisjointSet()

# create new trees
ds.find(1)
ds.find(2)

# link trees
ds.union(1, 2)

# DisjointSet contains single tree
#   1 -- 1
#     `- 2
ds  # displays DisjointSet(((1, 1), (1, 2)))
```

## Implementation

`DisjointSet` is the user facing implementation of Union-Find data structure.

As the name suggests, it exposes two methods:
* `union(x, y)`: link (optionally create) trees containing x and y.
* `find(x)`: find root or create tree containing x.

I also exposes the following dunders:
* `__bool__`: a DisjointSet is truthy if is contains at least one tree.
* `__eq__`: two DisjointSet are equal if they contain the same sets.
* `__iter__`: iterate over the sets in a DisjointSet set.
* `__repr__`: represent a DisjointSet in a reproducible way.

`DisjointSet` inherits from `BaseDisjointSet`, a simple implementation which
provides only the three base methods used to built Union-Find data structures.

These methods are protected (single underscore prefix), and assume their
preconditions are met before execution.

The three base methods are:
* `_make_set(x)`
    + effect: make a one node tree containing x.
    + precondition: no tree contains x.
* `_find_set(x)`
    + effect: find root of the tree containing x.
    + precondition: a tree contains x.
* `_union(x)`
    + effect: link the trees containing x and y into a single tree.
    + precondition: trees containing x and y are different.

## Copyright and License

Copyright (c) 2023 Louis Cochen \<louis.cochen@protonmail.ch\>

Licensed under the Apache License version 2.0, see LICENSE file.

## Contributing

At this time, this project is open source but not open contribution.
