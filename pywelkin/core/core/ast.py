#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception
import collections.abc

# from typing import List, Union, TypeVar, Tuple
import sys
from enum import Enum
from collections import defaultdict
from typing import Self, Union, Any, Optional
from lark import ast_utils, Token  # v_args, Token
from .graph import (
    InformationGraph,
    Label,
    LabelMember,
    LabeledConnectors,
    LabeledConnections,
)  # Connection, Tree, OutgoingNeighbors
from .tree import Tree
from .transformer import SignatureTransformer
from .validator import SemanticsValidator, SyntaxValidator

from dataclasses import dataclass

ast_module = sys.modules[__name__]

# TODO: Current goal, get local scope working (Base Welkin with no members, only units)
# Preferable: do not involve large tree libraries, but see what they do
# Members are just a way to write graphs in disguise (that CAN be extended, unlike normal graphs)
# Because of this, don't HAVE to parse elements directly, but that may be nice
# Most important thing: we need references to store connections
# TODO: look at tree implementation with a straightforward implementation of frontiers,
# OR at least of breadth first search (with the ROOT node)
# Alright, here's the plan: just use what Lark has. Let's not get overboard with some other library


# @dataclass
# class RelativeImport:
#     """Stores member's distance from current location to imported unit's location.
#     :param layers_up: Number of layers up where the unit is located
#     - Validation: must be contained in the total graph, see :class: core.validator.Validator
#     """
#
#     layers_up: int


class Validator(SemanticsValidator):
    @staticmethod
    def check_name_collisions(self, contents):
        # Check for name collisons
        # TODO: make sure contents is always hashable (check connector)
        contents_set = set(contents)
        if len(contents) != len(contents_set):
            raise SyntaxError("Name collision")
            # raise SyntaxError
        # for item in contents:
        #     # print("Input:", input, "\n")
        #     unique_label = item
        #     # Check for name collison
        #     if unique_ident == current_label and unique_label:
        #         print("Current syntax error")
        #         #raise SyntaxError
        #     current_ident = unique_ident

    @staticmethod
    def check_relative_member(self, contents):
        return False


# Reference: "A { B C { D E { F G H } } }"
class TerminalTransformer(SignatureTransformer):
    """Transforms terminals in Base Welkin to their machine represented values:
    - Sends identifiers to strings
    - Returns the values of units and elements
    - Returns the length of any dots in the type :class: RelativeImport"""

    def IDENT(self, token: Token):
        return token.value

    def UNIT(self, token: Token):
        label: Label = token.value
        return label

    def ELEMENT(self, token: Token):
        element_string = token.value
        element_value = element_string[1:]
        # TODO: make this more general with encodings
        if element_string.startswith("#"):
            element_value = float(element_value)
        return element_value

    def DOTS(self, token: Token):
        layers_up = len(token)
        return layers_up

    # @v_args(inline=True)
    # def start(self, token):
    #     return list(token)

    start = list


class _Ast(ast_utils.Ast):
    # Skip this class in ast_utils.Ast
    pass


class _BaseMember(LabelMember, _Ast, ast_utils.AsList):
    """Base subclass for Member rule, which checks whether the input label is empty."""

    def __init__(self, layers_up, path_list, label):
        # TODO: better integrate with validator!
        # For composition, could put something like _BaseMemberTransformer and LabelMember
        # as parameters to Relative, Absolute Member
        # Could add a separate component for linked lists (and put it in tree.py)
        if label == "_" and path_list:
            raise SyntaxError("Found empty string for member label.")
        elif label == "_":
            label = ""

        path: Optional[Tree[Label]] = Tree.from_list(path_list) if path_list else None

        super().__init__(layers_up, path, label)


# TODO: add meta information (for validation)
class RelativeMember(_BaseMember):
    # TODO: this is the validator's job! We need to make this clear while parsing
    # How does the validator work? It seems like a general mechanism,
    # or better yet, API that needs to be upheld
    def __init__(self, path_from_root: list[Label]):
        layers_up = path_from_root[0]
        label = path_from_root.pop()
        path_list = path_from_root[1:]

        super().__init__(layers_up, path_list, label)


class AbsoluteMember(_BaseMember):
    # TODO: this is the validator's job! We need to make this clear while parsing
    # How does the validator work? It seems like a general mechanism,
    # or better yet, API that needs to be upheld
    def __init__(self, path_from_root: list[Label]):
        layers_up = 0
        label = path_from_root.pop()
        path_list = path_from_root

        super().__init__(layers_up, path_list, label)


class Member(_Ast):
    pass


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

    def __init__(self, *args):
        self.kind = ArcKinds.edge
        super().__init__(*args)


class RightArrow(_Connector):
    kind = ArcKinds.right_arrow

    def __init__(self, *args):
        self.kind = ArcKinds.right_arrow
        super().__init__(*args)


class LeftArrow(_Connector):
    def __init__(self, args):
        self.kind = ArcKinds.left_arrow
        super().__init__(*args)


# ParsedOutgoingNeighbors = Dict[Label, List[Label]]
ParsedOutgoingNeighbors = dict


# # We need to distinguish PORTS; that's more important
# # So we better use a dict!
# If we use a list of tuples, then we could update
# the second entry, BUT we would have to merge it all later
class Connections(_Ast, ast_utils.AsList):
    # arcs: List[ParsedOutgoingNeighbors]
    # Note: in order to avoid creating a custom defaultdict type,
    # we are ignoring the original type of defaultdict's keys
    arcs: ParsedOutgoingNeighbors = defaultdict(lambda: defaultdict(list[LabelMember]))
    # TODO: change labels to a set!
    labels: list[Label] = []

    # TODO: make this work for general nested connections
    # In A - e -> B --> A - f -> B, we have two connectors
    # for A --> B. So we need to account for this in our logic!
    def add_connection(self, connection):
        initial, connector, final = connection

        self.labels += [initial, connector, final]

        connector_list = connector.value if connector.value else []

        match connector.kind:
            case ArcKinds.left_arrow:
                self.arcs[final][initial] += connector_list
            case ArcKinds.right_arrow:
                self.arcs[initial][final] += connector_list
            case ArcKinds.edge:
                self.arcs[final][initial] += connector_list
                self.arcs[initial][final] += connector_list

    def __init__(self, connections):
        # TODO: add validation.
        # Invalid example: A --> A --> A
        # This connection repeats itself!
        # (It doesn't add anything useful)
        while connections[2:]:
            connection = connections[:3]

            self.add_connection(connection)

            connections = connections[2:]

    #
    #     for i in range(3):
    #         match connection[i]:
    #             case Series(lst):
    #                 pass
    #             case _:
    #                 connection[i] = Series([connection[i]])
    #
    #     sources, connectors, targets = connection
    #
    #     [
    #         self.add_connection([source, connector, target])
    #         for source in sources.items
    #         for connector in connectors.items
    #         for target in targets.items
    #     ]

    def __repr__(self):
        return "Connections(arcs=" + str(dict(self.arcs)) + ")"


# A { B --> C }
# Tree(A, [Tree(B), Tree(C)])


class Vertex(_Ast):
    pass


@dataclass
class Series(_Ast, ast_utils.AsList):
    items: list


class Alias(_Ast):
    aliases: dict[Vertex, Vertex] = {}

    # TODO: add validation (alias names can't collide with
    # graph members)
    # Graph: need to do do traversal
    # Member case: straightforward
    def __init__(self, alias_vertex, original):
        aliases = {}

        match alias_vertex:
            case Graph():
                leaves = alias_vertex.get_leaves()
                for leaf in leaves:
                    aliases[leaf] = original
            case Member():
                aliases[alias_vertex] = original

        self.aliases = aliases

    def __repr__(self):
        return "Alias(aliases:" + str(self.aliases) + ")"


# TODO: figure out how to easily access nodes on ANY level, even if there are
# conflicting names
# Key: we need to get references in the tree!
# Aha! Attributes! Networkxx might come in handy here (or another tree library)
# BUT we also have to resolve node names... in lark.Tree, we would have to use
# some sort of numbers (and just keep track of them, i.e.,add those as "attributes")
# Alternatively, if we could access the hashed form, that might work better
class Graph(_Ast, ast_utils.AsList):
    # tree: Tree
    # connections: List[Connection]

    units: Tree[Label]
    connections: LabeledConnections = defaultdict(
        lambda: defaultdict(LabelMember, list[LabelMember])
    )
    name: Label
    labels: list[Label] = []
    member_aliases: dict[Member, Member] = defaultdict(Member)

    FlatItem = Union[Member, Alias, Connections, "Graph"]
    Series = list[FlatItem]
    Item = FlatItem | Series

    # TODO: add validation!
    def __init__(self, contents: list[Member | Self | Connections]):
        data = contents.pop(0)

        self.units = Tree(data, [])

        self.name = self.units.data

        for item in contents:
            self._add_item(item)

        # self.name = contents[0]
        # Include code to deal with series (lists in contents)
        # for item in contents[1:]:
        # if hasattr(item, "aliases"):
        #     self.member_aliases.update(item.aliases)
        #     for alias, original in item.aliases.items():
        #         self.member_aliases[alias] = original
        # elif hasattr(item, "name"):
        #     print("TODO")
        # elif hasattr(item, "arcs"):
        #     self.connections.update(item.arcs)
        # else:
        #     # if isinstance(item.namespace, RelativeImport):
        #     #     item.namespace.layers_up = item.namespace.layers_up - 1
        #     #     if item.namespace.layers_up < 0:
        #     #         raise SyntaxError("Undefined import.")
        #     self.connections.update({item: {}})

    def _add_item(self, item: Item):
        match item:
            case Series(lst):
                self._add_item(lst)
            case Alias(aliases):
                self.member_aliases.update(aliases)
                # TODO: validation is critical here! Don't repeat keys!
                self.labels += aliases.keys()
            case Connections(arcs):
                self.connections.update(arcs)
            # TODO: resolve mypy error with Self
            # case Graph(units, connections, name, labels, member_aliases):
            #     self.labels += labels
            #     self.units.children.append(units)
            case _:
                self.units.children.append(item)

    # TODO: decide whether to put into utils.py/dict.py

    def __repr__(self):
        return (
            "Graph(name="
            + self.name.__repr__()
            + ", member_aliases="
            + str(self.member_aliases)
            + ", units="
            + str(self.units)
            + ", connections="
            + str(dict(self.connections))
            + ")"
        )

    def depth_traversal(self) -> list[Vertex]:
        return self.tree.iter_subtrees_topdown()


# All non-atomic connections are stored with three entries;
# atomic connections only need two (because the connector is empty)
# Note that an edge "--" is treated as two arrows "<--" and "-->"

#         def list_to_linked_list(lst) -> Tree:
#             root = lst[0]
#             head = Tree(root, [])
#             current_child = head
#             descendants = lst[1:]
#             for descendant in descendants:
#                 print(descendant, head)
#                 current_child.children = Tree(descendant, [])
#                 current_child = current_child.children
#             return head
#     def graph(self, graph):
#         name: Label = graph[0] if graph[0] != "_" else False
#         contents = graph[1:]
#         print(contents)
#
#         return graph
#         #return self._parse_graph(name, contents)
#         # self.check_name_collisions(self, contents)
#
#         # Attempt to resolve relative imports
#         # self.check_imports(self, contents)
#
#         # Create edge lists for unit graph and connection graph
#         # print("Graph:", contents, "\n"
#
#     # series = list
#
#     series = list
#
#     def start(self, token):
#         print(token)
#         return token
#
#     # TODO; make start return the final graph
#     # def start(self, token):
#     #    # TODO: add debugging code. Returning list(token) gives an AST
#     #
#     #     #final_graph = InformationGraph()
#     #
#     #
#     #     return list(token)


# TODO: implement validation in Transformer
# In this case, we don't have that much to validate; we just need to check for name collisons. That's it!
# class Validator:
#     """Validate a base Welkin file. Only two conditions need to be checked: every graph may only be defined once and relative
#     members must be defined. (The first is essentially the One Definition Rule from C++)
#     """
