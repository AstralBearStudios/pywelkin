#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
from enum import Enum
from typing import TypeAlias, MutableSet

from ..graph import Label

from terms import member


class ArcKinds(Enum):
    edge = 0
    left_arrow = 1
    right_arrow = 2


class Connector:
    """Parsed representation of connectors.
    Parameters:
        kind: a value from :class ArcKinds:
        value: the corresponding :class Member:
    """

    kind: ArcKinds
    value: member.Base

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


class Edge(Connector):
    kind = ArcKinds.edge


class RightArrow(Connector):
    kind = ArcKinds.right_arrow


class LeftArrow(Connector):
    kind = ArcKinds.left_arrow


ArcTriple: TypeAlias = tuple[Label, Connector, Label]

# Subgraph = DuplicateCheckedSet[Label]


class ConnectionManager(MutableSet):
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
