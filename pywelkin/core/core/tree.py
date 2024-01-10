#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from typing import Self, Optional

import lark


class Tree[T](lark.Tree):
    """Tree data structure used in making base._Ast and graph.InformationGraph"""

    # Change type annotation to allow arbitrary data
    data: T

    @classmethod
    def from_list(cls, lst: list[T]) -> Self:
        """Converts a flat list :param lst:
        into a linked list (of type :class Tree:)."""
        root = lst[0]
        head = Tree(root, [])
        current = head
        for item in lst[1:]:
            current.children.append(Tree(item, []))
            current = current.children[0]

        return head

    def append_children(self, other: Self):
        """Appends children from the 'other' tree to current tree"""
        self.children += other.children

    def rooted_disjoint_union(self, root: Optional[Self], trees: list[Self]) -> Self:
        """Returns a new rooted tree with root :param new_root: and children :param trees:"""
        return Tree(root, trees)

    def replace_nodes(self, copy: bool = True):
        pass

    # Directly modified from lark.tree.Tree.iter_subtrees_topdown
    # (under the MIT license; see https://github.com/lark-parser/lark/blob/master/LICENSE)
    def get_leaves(self):
        """Gets leaves (non-Tree types or subtrees without children)"""
        leaves = []
        stack = [self]
        while stack:
            node = stack.pop()
            if not isinstance(node, Tree):
                leaves.append(node)
            elif not node.children:
                leaves.append(node)

        return leaves

    def step_bottom_up(self, frontier, next_vertices):
        """Checks whether each child of the root in frontier. If so,
        adds the root to the child's children and next_vertices

        Parameters:
            frontier
            next_vertices"""
        root = self.data
        for vertex in self.children:
            if vertex in frontier:
                vertex.children.append(root)
                next_vertices.append(root)
                break
