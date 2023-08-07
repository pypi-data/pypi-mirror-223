# Copyright 2023 Louis Cochen <louis.cochen@protonmail.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ufds.py: Union-Find Data Structure implementation."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


__version__ = "0.1.0"


class BaseDisjointSet(Generic[T]):
    """BaseDisjointSet implementation exposes unsafe primitives."""

    parent: dict[T, T]
    rank: dict[T, int]

    def __init__(self) -> None:
        self.parent = {}
        self.rank = {}

    def _make_set(self, x: T) -> T:
        """Unchecked make a one node tree containing x.

        Precondition: no tree contains x.
        """
        self.parent[x] = x
        self.rank[x] = 0
        return x

    def _find_set(self, x: T) -> T:
        """Unchecked find root of tree containing x.

        Precondition: a tree contains x.

        Optimised with with path compression.
        """
        if x != (px := self.parent[x]):
            px = self.parent[x] = self._find_set(px)
        return px

    def _union(self, x: T, y: T) -> None:
        """Unchecked link trees containing x and y into a single tree.

        Precondition: trees containing x and y are different.

        Optimised with ranked linking.
        """
        d = self.rank[x] - self.rank[y]
        if d < 0:
            self.parent[x] = y
        else:
            self.parent[y] = x
            if d == 0:
                self.rank[x] += 1


class DisjointSet(BaseDisjointSet[T]):
    """Concrete DisjointSet implementation with safe methods."""

    def __init__(self, seeds: Iterable[T | tuple[T, T]] = ()) -> None:
        super().__init__()
        for s in seeds:
            if not isinstance(s, tuple):
                s = s, s
            self.union(*s)

    def find(self, x: T) -> T:
        """Find root or create tree containing x."""
        if x not in self.parent:
            return self._make_set(x)
        return self._find_set(x)

    def union(self, x: T, y: T) -> None:
        """Link (optionally create) trees containing x and y."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        self._union(px, py)

    @property
    def _branches(self) -> Iterator[tuple[T, T]]:
        """Iterate over branches in trees."""
        for x in self.parent.keys():
            yield self._find_set(x), x

    def __bool__(self) -> bool:  # pragma: no cover
        """Alias to self.parent.__bool__ method."""
        return bool(self.parent)

    def __eq__(self, other: Any) -> bool:
        """Evaluate if forests are equivalent."""
        if not isinstance(other, type(self)):  # pragma: no cover
            return NotImplemented
        return sorted(tuple(self._branches)) == sorted(tuple(other._branches))

    def __iter__(self) -> Iterator[set[T]]:
        """Iterator over the trees in the forest."""
        trees: defaultdict[T, set[T]] = defaultdict(set)
        for p, c in self._branches:
            trees[p].add(c)
        yield from trees.values()

    def __repr__(self) -> str:
        return f"{type(self).__name__}({tuple(self._branches)!r})"
