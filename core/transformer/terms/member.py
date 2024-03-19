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
        if not member_str:
            return 0, None, ""

        # Check for relative member
        absolute_member_str = member_str.lstrip(".")

        layers_up = len(member_str) - len(absolute_member_str)

        path_list: list[str] = absolute_member_str.split(".")

        path_list = [float(item[1:]) if item[0] == "#" else item for item in path_list]

        path = Path(path_list)

        return layers_up, path
