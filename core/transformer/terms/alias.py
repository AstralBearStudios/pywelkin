#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from types import Vertex, Graph

from member import Base as Member


class AliasManager:
    aliases: list

    def __init__(self, alias_pairs: list[tuple[Vertex, Vertex]]):
        for alias_pair in alias_pairs:
            self.add(*alias_pair)

    def add(self, alias, original):
        max_layers_up = 0

        alias_list = []

        match alias:
            case Member():
                alias_list.append(alias)
            case Graph():
                alias_list = alias.get_leaves()

        for item in alias_list:
            max_layers_up = max(item.layers_up, original.layers_up)
            self.aliases[max_layers_up].add(item)
