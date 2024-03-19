#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import itertools
from typing import Generic, Iterable, TypeVar, Optional, Self


class NestedDict(dict):
    """Nested dictionary of arbitrary depth.
    Each leaf is an empty :class NestedDict:.

    Any method with a parameter :param keys:
    takes in an iterable. Takes in
    non-iterable as a singleton.
    """

    def __init__(self, *args, **kwargs):
        super(NestedDict, self).__init__(*args, **kwargs)

    def __getitem__(self, keys: Iterable):
        # TODO: remove this check; it is a bit messy
        # We only want to do this for single item objects
        if not isinstance(keys, Iterable):
            keys = (keys,)
        result = self
        for key in keys:
            result = result.setdefault(key, {})
        return result

    def __setitem__(self, keys, value):
        if not isinstance(keys, Iterable):
            keys = (keys,)
        head = self
        iterator = itertools.chain(keys, value)
        for node in iterator:
            head = head.setdefault(node, {})


RootType = TypeVar("RootType")
MappedValueType = TypeVar("MappedValueType")


# TODO: refactor RootedMapping for AST
class RootedMapping:
    """Mapping with a special, external element :param root:."""

    root: RootType

    map: dict[int, MappedValueType] = {}

    def __init__(
        self, root: Optional[RootType], map: Optional[dict[int, MappedValueType]]
    ):
        self.root = root
        self.map = map

    def __getitem(self, index: int):
        if index == 0:
            return self.root
        else:
            return self.map.setdefault(index, None)


Node = TypeVar("Node")


class Tree(Generic[Node]):
    """Tree data structure used in making :class _AST: and :class InformationGraph:

    Paramaters:
        root
        branches
    """

    root: Optional[Node]
    branches: NestedDict[Node]

    def __init__(
        self, root: Optional[Node] = None, branches: Optional[NestedDict] = None
    ):
        self.root = root
        self.branches = branches or NestedDict()

    def __getitem__(self, branch: Iterable[Node]):
        """Retrieves a node via an iterable.

        Example:
            >>> tree = Tree(root = "A")
            >>> tree["A", "B"]
                ("A", {"B" : {"C" : {}}})

        If the item is not found, returns an empty dict
        and adds :param branch: to :param branches:.

        Example:
            >>> tree["E", "F"]
                {}
            >>> tree
                ("A", {"E" : {"F" : {}}})
        """
        return self.branches[branch]

    def __setitem__(self, branch: Iterable[Node], leaf: Node):
        """Stores an iterable in :param branches:.
        Example:
            >>> tree = Tree(root="A")
            >>> tree[(1, 2, 3)] = 4
                branches={1: {2: {3: {4: {}}}}}
        """
        self.branches[branch] = leaf

    @classmethod
    def append_branches(self, other: Self):
        """Appends branches from :param other: tree to current tree."""
        self.branches |= other.branches

    @classmethod
    def rooted_disjoint_union(cls, root: Node, trees: Iterable[Self]) -> Self:
        """Returns a new rooted tree with root :param new_root: and children :param trees:".
        Only use for trees with distinct roots.""
        branches = NestedDict()
        """

        branches = NestedDict()

        for tree in trees:
            branches[[tree.root]] = tree.branches

        return cls(root, branches)

    def get_leaves(self):
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
        """Checks whether each child of the root in frontier.
        If so, adds the root to the child's branches and next_vertices' branches.

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
