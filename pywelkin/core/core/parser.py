#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from typing import Protocol, Optional, Dict, Callable

from lark.lark import Lark, Token
from lark.lexer import Lexer
from lark.visitors import Transformer

from .validator import ErrorHandler
from .tree import Tree


# class InteractiveParse(Protocol):
#     parse: str


class Parser:
    """Main interface to Lark for parsing context free grammars"""

    parser: Lark
    lexer: Lexer
    error_handler: Optional[ErrorHandler]
    transformer: Optional[Transformer]
    start: str
    strict: bool
    lalr: bool
    debug: bool

    def __init__(
        self,
        grammar: str,
        tree_class: Optional[Tree] = None,
        error_handler: Optional[ErrorHandler] = None,
        transformer: Optional[Transformer] = None,
        start: str = "start",
        strict: bool = True,
        debug: bool = True,
        lalr: bool = True,
        cache: bool = True,
    ) -> None:
        self.start = start
        self.strict = strict
        self.debug = debug
        self.lalr = lalr
        self.cache = cache

        if self.lalr:
            self.error_handler = error_handler

        inline_transformer = transformer if lalr else None

        self.parser = Lark.open(
            grammar_filename=grammar,
            rel_to=__file__,
            parser="lalr",
            start=start,
            strict=self.strict,
            debug=self.debug,
            propagate_positions=True,
            maybe_placeholders=False,
            regex=True,
            transformer=inline_transformer,
            tree_class=tree_class,
        )

    def parse(self, input: str):
        if self.lalr and self.error_handler:
            on_error_function = self.error_handler.run
        else:
            on_error_function = None
        tree = self.parser.parse(input, on_error=on_error_function)
        if not self.lalr and self.transformer:
            tree = self.transformer.transform(tree)
        return tree
