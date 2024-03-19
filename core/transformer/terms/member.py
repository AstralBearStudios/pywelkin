#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from dattaclasses import dataclass

from ...containers import Tree, Path
from ...graph import Label


@dataclass
class LabelTree:
    """Base class for adding :param labeltree:.
    Essential component of :class Member:."""

    label_tree: Tree[Label]


class Base:
    """Base class for Member with key parameters."""

    layers_up: int
    path: tuple[Label]
    value: Label

    def __hash__(self):
        return hash((self.layers_up, self.path, self.value))


class Parser:
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
