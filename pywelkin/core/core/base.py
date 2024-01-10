#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from lark import ast_utils
from .parser import Parser
from .ast import ast_module, TerminalTransformer


class SemanticValidator:
    pass


class Recorder:
    """Stores the information from a WIG into its canonical string"""

    def bottom_up_step(self, graph):
        raise NotImplementedError

    def get_canonical_string(self, graph) -> str:
        """Return the canonical string of an InformationGraph."""
        raise NotImplementedError


class Base:
    """Converts a valid Base Welkin file into a compact binary form"""

    strict: bool
    debug: bool
    recorder: Recorder = Recorder()

    def __init__(self, strict: bool = True, debug: bool = True):
        self.parser = Parser(
            grammar="grammars/base.lark",
            strict=strict,
            debug=debug,
            transformer=ast_utils.create_transformer(ast_module, TerminalTransformer()),
        )
