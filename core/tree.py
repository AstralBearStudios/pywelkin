#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from typing import Self, TypeVar, Generic, Iterable, Optional

import pprint

from .utils import NestedDict

T = TypeVar("T")


class Tree(Generic[T]):
    """Tree data structure used in making :class _Ast: and :class InformationGraph:

    Parameters:
        root
        branches
    """

    root: T
    branches: NestedDict[T]

    def __init__(self, root: T, branches: Optional[NestedDict] = None):
        self.root = root
        self.branches = branches or NestedDict()

    def __getitem__(self, branch: Iterable[T]):
        """Retrieves a node via an iterable.

        Example:
            >>> tree = Tree(root="A")
            >>> tree["A", "B"] = "C"
            >>> tree["B", "C"]
                ("A", {"B" : {"C": {}}})

        If the item is not found, returns an empty dict
        and adds :param branch: to :param branches:

        Example:
            >>> tree["E", "F"]
                {}
            >>> tree
                ('A', {'E': {'F': {}}})
        """
        return self.branches[branch]

    def __setitem__(self, branch: Iterable[T], leaf: T):
        """Stores an iterable in :param branches:.
        Example:
            >>> tree = Tree(root="A")
            >>> tree[(1, 2, 3)] = 4
                branches={1: { 2: { 3: {4: {}} } }
            >>> tree[["A", "B", "C"]] = "D"
                branches={"A": {"B": {"C": {"D": {}}}}}

        The easiest way is to write a path without
        parantheses/brackets.
            >>> tree[1, 2, 3] = 4
                branches={1: { 2: { 3: {4: {}} } }
        """
        self.branches[branch] = leaf

    @classmethod
    def from_list(cls, lst: list[T]) -> Self:
        """Converts a flat list :param lst:
        into a linked list."""
        root = lst[0]
        path = lst[1:-1]
        leaf = lst[-1]

        branches = NestedDict()

        branches[path] = leaf

        return cls(root, branches)

    def append_branches(self, other: Self):
        """Appends branches from the :param other: tree to current tree"""
        self.branches |= other.branches

    @classmethod
    def rooted_disjoint_union(cls, root: T, trees: Iterable[Self]) -> Self:
        """Returns a new rooted tree with root :param new_root: and children :param trees:
        Only use for trees with distinct roots.
        """
        branches = NestedDict()

        for tree in trees:
            branches[[tree.root]] = tree.branches

        return cls(root, branches)

    def get_leaves(self):
        """Gets leaves (branches with no children)."""
        leaves = []
        stack = list(self.branches.items())

        while stack:
            branch, children = stack.pop()
            if children:
                stack.extend(children.items())
            else:
                leaves.append(branch)

        return leaves

    def step_bottom_up(self, frontier, next_vertices):
        """Checks whether each child of the root in frontier. If so,
        adds the root to the child's branches and next_vertices' branches.

        Parameters:
            frontier
            next_vertices
        """
        for vertex, _ in self.branches:
            if vertex in frontier:
                vertex[self.root] = NestedDict()
                next_vertices[self.root] = NestedDict()
                break

    def __str__(self):
        return str((self.root, self.branches))

    def __repr__(self):
        return "Tree(root=" + str(self.root) + ", branches=" + str(self.branches) + ")"
