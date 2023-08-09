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

"""test_ufds.py: Test Union-Find Data Structure implementation."""

import ufds


def test_path_compression():
    actual = ufds.DisjointSet([0, 1, 2])
    actual.union(0, 1)
    actual.union(1, 2)
    expected = ufds.DisjointSet([0, 1, 2])
    expected.union(0, 1)
    expected.union(0, 2)
    assert actual == expected


def test_ranked_union():
    ds = ufds.DisjointSet([(0, 1), (2, 3), (4, 5), (1, 2), (4, 3)])
    assert ds.parent[4] == 0
    assert ds.rank[0] == 2


def test_iter():
    ds = ufds.DisjointSet([(0, 1), (2, 3), (4, 5), (1, 2)])
    assert list(iter(ds)) == [{0, 1, 2, 3}, {4, 5}]


def test_repr():
    expected = ufds.DisjointSet([(0, 1), (2, 3), (4, 5), (1, 2)])
    actual = eval("ufds." + repr(expected))
    assert actual == expected
