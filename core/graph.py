#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from typing import Optional, TypeVar, TypeAlias, Generic
from collections import defaultdict
from enum import Enum
from dataclasses import dataclass, field

from .tree import Tree


# TODO: generalize these to different codecs
Label = str | float


T = TypeVar("T")


@dataclass
class LabelMap(Generic[T]):
    """A mapping of labels to nodes, together with the set of labels used for fast access.

    Parameters:
        labels
        aliases
        mapping
    """

    labels: set[Label] = field(default_factory=set)
    aliases: dict[Label, Label] = field(default_factory=dict)
    mapping: dict[Label, T] = field(default_factory=dict)


Connectors = list[T]


# TODO: the transformer should turn a parse graph into a AbstractBigraph. DO NOT include that code here!
class AbstractBigraph:
    """Interface to the Welkin Information Graph (WIG). Does not provide concrete implementations.

    Parameters:
        units
        connections
    """

    # """The Welkin Information Graph (WIG) data structure that can be stored and traversed.
    # This does not contain any additional instructions on how to traverse the graph.

    units: Tree[T]
    connections: dict[T, dict[T, Connectors]] = {}
    _canonical_string: str

    def __init__(self, units: Tree[T], connections: dict[T, dict[T, Connectors]]):
        self.units = units
        self.connections = connections

    def ___eq__(self, other):
        try:
            return self.units == other.units and self.connections == other.connections
        except AttributeError:
            return False

    def __str__(self):
        return str((self.units, self.connections))

    def __repr__(self):
        return (
            "AbstractBigraph(units="
            + str(self.units)
            + ", connections="
            + str(self.connections)
            + ")"
        )

    def __rich__(self):
        pass

    # TODO: generalize to different encoding schemes.
    # Maybe involve BNF in this?
    def canonical_string(self) -> str:
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
        canonical_string: str = "r0" + ":"
        # Set frontier to set inner faces
        # This means we want to use [0], because
        # there are no inner faces
        frontier = [0]
        next_vertices = []
        current_root = None
        while not frontier:
            self.units.step_bottom_up(frontier, next_vertices)
            frontier = next_vertices
            canonical_string += self._frontier_encoding(self, frontier)
            next_vertices = []
        canonical_string.join("#")

        canonical_string += self._connection_encoding()
        self._canonical_string = canonical_string

    @staticmethod
    def _frontier_encoding(self, frontier) -> str:
        frontier_encoding: str = ""
        for vertex in frontier:
            print(vertex)

        frontier_encoding.join("#")
        return frontier_encoding

    def _connection_encoding(self) -> str:
        return ""


Vertex = tuple[int]


class ConcreteBigraph(AbstractBigraph):
    """ConcreteInformationGraph uses numbers in the underlying units.
    Units are labeled per graph starting from 0.
    Members are distinguished using paths to a parent"""

    pass


class InformationGraph:
    label_tree: LabelMap
    graph: AbstractBigraph
