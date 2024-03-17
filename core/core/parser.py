#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

from typing import Protocol, Optional, Dict, Callable

from lark import Lark, Token, Transformer
from lark.lexer import Lexer

from .validator import ErrorHandler
from .tree import Tree


class Parser:
    """Main interface to Lark for parsing context free grammars. Prioritizes
    LALR grammars, but provides the Earley parser as a choice."""

    parser: Lark
    lexer: Lexer
    error_handler: Optional[ErrorHandler]
    transformer: Optional[Transformer]
    start: str
    strict: bool
    is_lalr: bool
    debug: bool
    cache: bool | str

    def __init__(
        self,
        grammar: str,
        is_lalr: bool = True,
        tree_class: Optional[Tree] = None,
        error_handler: Optional[ErrorHandler] = None,
        transformer: Optional[Transformer] = None,
        start: str = "start",
        strict: bool = True,
        debug: bool = True,
        cache: bool | str = True,
    ) -> None:
        self.start = start
        self.strict = strict
        self.debug = debug
        self.is_lalr = is_lalr
        self.cache = cache

        parser_kind = "lalr" if is_lalr else "earley"

        self.error_handler = error_handler if self.is_lalr else None

        inline_transformer = transformer if is_lalr else None

        self.parser = Lark.open(
            grammar_filename=grammar,
            rel_to=__file__,
            parser=parser_kind,
            start=start,
            strict=self.strict,
            debug=self.debug,
            propagate_positions=True,
            maybe_placeholders=True,
            regex=False,
            transformer=inline_transformer,
            tree_class=tree_class,
        )

    def parse(self, text: str):
        if self.is_lalr and self.error_handler:
            on_error_function = self.error_handler.run
        else:
            on_error_function = None

        tree = self.parser.parse(text, on_error=on_error_function)

        if not self.is_lalr and self.transformer:
            tree = self.transformer.transform(tree)

        return tree
