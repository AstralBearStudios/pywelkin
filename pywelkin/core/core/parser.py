# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from typing import Protocol, Optional

from lark.lark import Lark
from lark.lexer import Lexer
from lark.visitors import Transformer


class Tree(Protocol):
    pass


class InteractiveParse(Protocol):
    parse: str


class ErrorHandler(Protocol):
    errors: dict[str, str]

    def run(self, error) -> bool:
        """Runs the error handler on an individual token and checks how to respond to error"""
        raise NotImplementedError


class Parser:
    """Main interface to Lark for parsing context free grammars"""

    parser: Lark
    lexer: Lexer
    transformer: Optional[Transformer]
    strict: bool
    lalr: bool
    debug: bool

    def __init__(
        self,
        grammar: str,
        tree_class: Tree,
        error_handler: Optional[ErrorHandler] = None,
        transformer: Optional[Transformer] = None,
        start: str = "term",
        strict: bool = True,
        debug: bool = True,
        lalr: bool = True,
        cache: bool = True,
    ) -> None:
        self.strict = strict
        self.debug = debug
        self.lalr = lalr
        self.cache = cache

        inline_transformer = transformer if lalr else None

        self.parser = Lark(
            grammar=grammar,
            on_error=error_handler,
            start=start,
            strict=self.strict,
            debug=self.debug,
            propogate_positions=True,
            regex=True,
            transformer=inline_transformer,
            tree_class=tree_class,
        )

    def parse(self, input: str):
        tree = self.parser.parse(input)
        if not self.lalr and self.transformer:
            tree = self.transformer.transform(tree)
        return tree

    def parse_interactive(self, input: str):
        self.parser.parse_interactive(input)
