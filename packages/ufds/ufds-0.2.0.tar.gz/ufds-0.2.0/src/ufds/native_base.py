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

"""base.py: Union-Find Data Structure base implementation."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


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
