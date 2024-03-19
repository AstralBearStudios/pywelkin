#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import collections.abc

# from typing import List, Union, TypeVar, Tuple

import sys
from typing import Self, Union, Optional, TypeVar, Generic
from dataclasses import dataclass

from lark.ast_utils import Ast, AstList

from .containers import NestedDict
from .exceptions import NameCollisionError
from .tree import Tree
from .graph import (
    # InformationGraph,
    Label,
    LabelMap,
)

from ...terms import member


ast_module = sys.modules[__name__]

# Base Pipeline
# Gather --> Order --> Format/Propagate --> Combine --> Toplevel Validation
# 1. Gather information needed from each token into temporary forms
# - Validate as much as possible with local information
# 2. Order terms based on max_layers_up
# 3. Work with all terms
# 4. Combine all terms in a graph
# 5. Validate toplevel: check there are no members with non-zero layers_up


class Member(Ast, member.Base):
    """Class for member rule, which converts any terminals (as lists
    or strings) into the appropriate parameters.

    Parameters:
        layers_up
        path
        value
    """

    def __init__(self, member_str):
        member_data = member.Parser.from_str(member_str)
        layers_up, path, value = member_data

        super().__init__(layers_up, path, value)


@dataclass
class Series(Ast):
    """Puts terms into a list :param lst."""

    lst: list


class Connections(Ast, AstList):
    """Connections rule in grammars/base.lark.

    Raises:
        :class NameCollision: when connections are repeated in a row.
        For example, "A --> A --> A" is invalid, because
        the connection "A --> A" is repeated twice
    """

    labels: set[Label] = set()
    arcs: dict[Label, dict[Label, set[Label]]] = {}

    def __init__(self, connections):
        # print(connections)
        while connections[2:]:
            connection = connections[:3]

            self.add_connection(connection)

            connections = connections[2:]

    def __repr__(self):
        return (
            "Connections(labels="
            + str(self.labels)
            + "arcs="
            + str(dict(self.arcs))
            + ")"
        )


# D { A := B } D.B := C
# TODO: implement chaining
# Right now, the user could say "A := B", and
# then later on, "B := C"
# Because of relative imports upwards, this means
# we have to store aliases as pairs
# THAT's why we want validation
class Alias(Ast):
    labels: set[Label] = set()
    aliases: dict[Label, Label]
    original: Label

    def __init__(self, alias_vertex, original):
        self.original = original

        labels = set()
        labels.add(original.value)

        aliases = {}
        current_vertex = None

        match alias_vertex:
            case Graph():
                leaves = alias_vertex.get_leaves()
                for leaf in leaves:
                    if leaf == current_vertex:
                        raise NameCollisionError(leaf)
                    labels.union(leaf)
                    aliases[leaf] = original
                    current_vertex = leaf
            case Member():
                labels.add(alias_vertex.value)
                full_path = alias_vertex.path or []
                full_path.append(alias_vertex.value)
                aliases[full_path] = original

        self.labels = labels
        self.aliases = aliases


FlatItem: TypeAlias = Union[Member, "Graph", Alias, Connections]
Item: TypeAlias = FlatItem | Series


class Graph(_Ast, ast_utils.AsList):
    label_map: LabelMap = LabelMap()
    label_tree: Tree[Label]
    connections: dict[Label, dict[Label, list[Label]]] = {}

    name: Label | Member
    member_aliases: dict[Member, Member] = {}
    imported_members: list[Member] = []

    # TODO: add validation!
    def __init__(self, contents: list[Member | Self | Connections]):
        # First element in a graph is always its name
        root = contents.pop(0) or ""

        self.units = Tree(root)
        self.name = root

        for item in contents:
            self.add_item(item)

    def add_item(self, item: Item):
        match item:
            # TODO: determine how this case could be refactored
            # Maybe use a loop in __init__?
            case Series(lst):
                for lst_item in lst:
                    self.add_item(lst_item)
            case Alias(labels, aliases, mapping, original):
                for alias, value in aliases.keys():
                    if alias in self.member_aliases:
                        # TODO: add error details on original alias value vs new one
                        raise NameCollisionError(alias)
                    self.member_aliases[alias] = value
                    # TODO: validation is critical here! Don't repeat keys!
                    self.label_map.labels += aliases.keys()
            case Connections():
                pass
                # self.connections.update(arcs)
            # TODO: resolve mypy error with Self
            # case Graph(units, connections, name, labels, member_aliases):
            case _:
                if hasattr(item, "units"):
                    member = item.name
                else:
                    member = item

                print(member)

                self.label_map.labels.add(member.value)

                self.add_member(member)

    def add_member(self, member: Member):
        if member.layers_up == 0:
            if member.path:
                self.units[member.path] = member.value
            else:
                self.units[member.value] = NestedDict()

        else:
            self.imported_members.append(member)

    # TODO: decide whether to put into utils.py/dict.py

    def __repr__(self):
        return (
            "Graph(label_map="
            + str(self.label_map)
            + ", units="
            + str(self.units)
            + ", connections="
            + str(dict(self.connections))
            + ", imported_members="
            + str(self.imported_members)
            + ")"
        )

    # def depth_traversal(self) -> list[Vertex]:
    #     return self.tree.iter_subtrees_topdown()


# def _FinalTransformer(Transformer):
#     def start():
#         pass
