# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Creates the tools for base Welkin, which is simply a way to store information

from .parser import Parser
from .tree import InformationTree
from lark.visitors import Transformer

from dataclasses import dataclass


@dataclass
class Unit:
    name: str


@dataclass
class Atom:
    value: str | float
    pass


class InformationTransformer(Transformer):
    """Transforms a valid base Welkin file into an InformationTree in Lark."""

    def WORD(self, token):
        return token.value

    def NUMBER(self, token):
        return token.update(value=float(token))

    def unit(self, token):
        return Unit(token)

    def num(self, token):
        (value,) = token
        return value

    def string(self, token):
        (s,) = token
        return s[1:-1]

    def atom(self, token):
        (value,) = token
        return value

    def graph(self, token):
        """Validates that there are no name collisons in a given graph."""
        # print("Printing token:", token, "\n")

        unique_ident = None
        current_ident = None
        graph_list = []
        for input in token:
            # print("Input:", input, "\n")
            unique_ident = input
            if unique_ident == current_ident and unique_ident:
                raise SyntaxError
            graph_list.append(unique_ident)
            current_ident = unique_ident
        return graph_list

    def connection(self, token):
        init, connector, final = token
        if init == final:
            # Creates a loop
            return (init, connector)
        else:
            return (init, connector, final)

    def edge(self, token):
        return token

    def left_arrow(self, token):
        return token

    def right_arrow(self, token):
        return token

    def term(self, token):
        (value,) = token
        return value

    def start(self, token):
        """Validates that there are no name collisons, and returns term if it is valid"""
        (value,) = token
        return value


# TODO: implement validation in Transformer
# In this case, we don't have that much to validate; we just need to check for name collisons. That's it!
# class Validator:
#    """Validate a base Welkin file. Only one condition needs to be checked: every graph may only be defined once. This is essentially
#    the equivalent of the One Definition Rule from C++"""


class Serializer:
    """Serialize a valid Welkin file"""

    pass


class Recorder:
    """Stores the information in a base welkin file into a compact binary form, similar to a SQLite database"""

    strict: bool
    debug: bool

    def __init__(self, strict: bool = True, debug: bool = False):
        self.parser = Parser(
            grammar="grammars/base.lark",
            strict=strict,
            debug=debug,
            transformer=InformationTransformer()
            # tree_class=InformationTree,
        )
