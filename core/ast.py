#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import collections.abc

# from typing import List, Union, TypeVar, Tuple

import sys
from typing import Self, Union, Optional, TypeVar, TypeAlias, Generic
from enum import Enum
from collections import defaultdict
from lark import ast_utils, Token  # v_args, Token
from .exceptions import NameCollisionError, ArgumentError
from .graph import (
    InformationGraph,
    Label,
    LabelMap,
)
from .tree import Tree
from .exceptions import NameCollisionError
from .validator import SemanticsValidator, SyntaxValidator
from .containers import NestedDict

from dataclasses import dataclass

ast_module = sys.modules[__name__]


class _Ast(ast_utils.Ast):
    # Underscores mean ast_utils.Ast should skip this class
    pass


@dataclass
class _BaseMember:
    """Base class for Member with key parameters"""

    layers_up: int
    path: tuple[Label]
    value: Label

    def __hash__(self):
        return hash((self.layers_up, self.path, self.value))


class _ParseMember:
    """Parses the result from a member string.
    Temporarily added until alternative solution is found for
    transforming concatenated terminals in lark.
    """

    @classmethod
    def from_str(cls, member_str: str) -> tuple:
        layers_up = 0

        while member_str[0] == ".":
            layers_up += 1
            member_str = member_str[1:]

        path_list: list[str] = member_str.split(".")

        # print(path_list)

        path_list = [float(item[1:]) if item[0] == "#" else item for item in path_list]

        value = path_list.pop()

        path = Tree.from_list(path_list) if path_list else None

        return layers_up, path, value


class Member(_Ast, _BaseMember):
    """Class for member rule, which converts any terminals (as lists
    or strings) into the appropriate parameters.

    Parameters:
        layers_up
        path
        value
    """

    def __init__(self, member_str):
        member_data = _ParseMember.from_str(member_str)
        layers_up, path, value = member_data

        super().__init__(layers_up, path, value)


@dataclass
class Series(_Ast, ast_utils.AsList):
    list: list


class ArcKinds(Enum):
    edge = 0
    left_arrow = 1
    right_arrow = 2


class _Connector(_Ast):
    """Parsed representation of connectors.
    Parameters:
        kind: a value from :class ArcKinds:
        value: the corresponding :class Member:
    """

    kind: ArcKinds
    value: Member

    def __init__(self, *args):
        self.value = args[0] if args else None

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(kind="
            + self.kind.__repr__()
            + ", value="
            + self.value.__repr__()
            + ")"
        )


class Edge(_Connector):
    kind = ArcKinds.edge


class RightArrow(_Connector):
    kind = ArcKinds.right_arrow


class LeftArrow(_Connector):
    kind = ArcKinds.left_arrow


class Connections(_Ast, ast_utils.AsList):
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

    def add_arrow(self, initial, connector, final):
        try:
            added_connector_set = connector.value
        except AttributeError:
            added_connector_set = set()

        # if not self.arcs[initial][final].isdisjoint(added_connector_set):
        #     raise NameCollisionError((initial, connector, final))

        self.arcs.setdefault(initial, {}).setdefault(final, set()).union(
            added_connector_set
        )

    def add_connection(self, connection):
        initial, connector, final = connection

        self.labels.union((initial.value, final.value))

        if connector.value:
            self.labels.update(connector.value)

        try:
            added_connector_set = connector.value
        except AttributeError:
            added_connector_set = set()

        # Edge case: if initial = final, just make it a left arrow
        # This avoids duplicate dictionary assignments
        if initial == final:
            connector.kind = ArcKinds.left_arrow

        match connector.kind:
            case ArcKinds.left_arrow:
                self.add_arrow(final, connector.value, initial)
            case ArcKinds.right_arrow:
                self.add_arrow(initial, connector.value, final)
            case ArcKinds.edge:
                self.add_arrow(final, connector.value, initial)
                self.add_arrow(initial, connector.value, final)

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
class Alias(_Ast):
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
