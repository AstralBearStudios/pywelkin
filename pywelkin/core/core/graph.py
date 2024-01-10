#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from collections import defaultdict
from enum import Enum
from typing import Union, Optional
from dataclasses import dataclass, field

from .tree import Tree


class Port(Enum):
    Source = 0
    Connector = 1
    Target = 2


# TODO: override data in this Tree class (mostly for type checking)
# noinspection PyRedeclaration


@dataclass
class Member[T]:
    """
    Parameters:
        layers_up: distance from the current position to the specified unit
        path
        value
    """

    layers_up: int
    path: Optional[Tree[T]]
    value: T
    aliases: list[Union[float, str]] = field(default_factory=lambda: [])

    def __hash__(self):
        return hash((self.layers_up, self.path, self.value))

    def __repr__(self):
        return (
            self.__class__.__name__
            + "(layers_up="
            + str(self.layers_up)
            + ", path="
            + str(self.path)
            + ", unit="
            + str(self.value)
            + ")"
        )


Label = Union[float, str]

LabelMember = Member[Label]
LabeledConnectors = list[LabelMember]
LabeledConnections = dict[LabelMember, dict[LabelMember, list[LabelMember]]]


@dataclass
class LabelingSet[T]:
    labels: list[Label]
    aliases: dict[Label, Label]
    map: dict[LabelMember, T]


# OutgoingNeighbor = Tree
# Connector = Tree
# OutgoingNeighbors = dict[Label, List[Connector]]
# Connection = Tuple[Tree, Optional[Tree], Tree]


# @dataclass
# class ParseGraph:
#     """Abstract Syntax Graph for Welkin, containing the label tree and
#     outgoing neighbors rom the label tree's root
#     """
#     tree: Tree
#     outgoing_neighbors: OutgoingNeighbors


class InformationGraph[T]:
    """Interface to the Welkin Information Graph (WIG). Does not provide concrete implementations.

    Parameters:
    labels
    units
    connections
    """

    # """The Welkin Information Graph (WIG) data structure that can be stored and traversed.
    # This does not contain any additional instructions on how to traverse the graph.

    units: Tree[T]
    label_set: LabelingSet[Member[T]]  # list[dict[Member[T], Label]]

    Connectors = list[T]
    connections: dict[T, dict[T, Connectors]] = defaultdict(
        lambda: defaultdict(list[T])
    )
    _canonical_string: str

    def __init__(
        self,
        label_trees: list[Tree[LabelMember]],
        label_maps: list[dict[LabelMember, T]],
        connections: LabeledConnections,
    ):
        # Recursively map through label paths to units

        # self.labels = [
        #     filter(lambda label: label_map[label], label_tree)
        #     for label_tree in label_trees
        #     for label_map in label_maps
        # ]
        # self.units = label_tree
        self.connections = connections

    def ___eq__(self, other):
        try:
            return self.units == other.units and self.connections == other.connections
        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.labels, self.units, self.connections, self._canonical_string))

    def __rich__(self):
        pass

    # TODO; generalize to different encoding schemes.
    # Maybe involve BNF in this?
    def get_canonical_string(self) -> str:
        if not self._canonical_string:
            self._generate_canonical_string()
        return self._canonical_string

    def _generate_canonical_string(self):
        """Returns the InformationGraphs' canonical string encoding.
        Adapted from Dominik Grzelak and Uwe Aßmann's paper
        "A Canonical String Encoding for Pure Bigraphs"."""

        # For simplicity, we use a fixed encoding for each vertex.
        # This will be prefixed on every canonical string and
        # can be given
        canonical_string: str = "r" + str(len(self.controls)) + ":"
        frontier = [0]
        next_vertices = []
        current_root = None
        while not frontier:
            self.units.step_bottom_up(frontier, next_vertices)
            frontier = next_vertices
            canonical_string += self._frontier_encoding(frontier)
            next_vertices = []
        canonical_string.join("#")

        canonical_string += self._connection_encoding()
        self._canonical_string = canonical_string

    def _frontier_encoding(self, frontier) -> str:
        frontier_encoding: str = ""
        for vertex in frontier:
            print(vertex)

        frontier_encoding.join("#")
        return frontier_encoding

    def _connection_encoding(self) -> str:
        return ""


VertexRepresentation = int


class ConcreteInformationGraph[VertexRepresentation](InformationGraph):
    """ConcreteInformationGraph uses numbers in the underlying units.
    Units are labeled per graph starting from 0.
    Members are distinguished using paths to a parent"""

    pass
