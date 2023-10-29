# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Creates the tools for base Welkin, which is simply a way to store information

from parser import Parser
from tree import InformationTree


class Validator:
    """Validate a base Welkin file. Only two main conditions need to be met: no identifiers can solely be the symbols
    -, <, >, {, or }, and in a given scope, every graph may only be defined once."""


class Serialize:
    """Serialize a valid Welkin file"""

    pass


class Recorder:
    """Stores the information in a base welkin file into a compact binary form, similar to a SQLite database"""

    strict: bool
    debug: bool

    def __init__(self, strict: bool = True, debug: bool = False):
        self.parser = Parser(
            grammar="./grammars/base.welkin",
            strict=strict,
            debug=debug,
            tree_class=InformationTree,
        )
