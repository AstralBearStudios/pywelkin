# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from lark import visitors
from lark.visitors import Transformer

from .parser import Parser, ErrorHandler

# from .tree import ExecutableTree


class SyntaxErrorHandler(ErrorHandler):
    """Handles syntax errors produced by in a standard Welkin file"""

    errors: dict[str, str] = {}

    def run(self, error) -> bool:
        raise NotImplementedError


class ExecutableTransformer(Transformer):
    """Turns an AST from standard Welkin into an ExecutableTree"""

    def graph(self, expr):
        pass


# TODO: implement validation in Transformer
# In this case, we don't have that much to validate; we just need to check for name collisons. That's it!
class Validator:
    """Validate a base Welkin file. Only one condition needs to be checked: every graph may only be defined once. (This is essentially
    the One Definition Rule from C++)"""


class Attributor:
    """Assigns attributes valid Attribute Welkin"""

    parser: Parser
    engine: visitors.Interpreter
    strict: bool
    debug: bool

    def __init__(self, strict: bool = True, debug: bool = False):
        self.strict = strict
        self.debug = debug
        self.parser = Parser(
            grammar="./grammars/attribute.lark",
            error_handler=SyntaxErrorHandler(),
            transformer=ExecutableTransformer(),
            strict=strict,
            debug=debug,
            # tree_class=ExecutableTree,
        )
        self.validator = Validator()
        self.engine = visitors.Interpreter()

    def run(self, tree):
        """Runs the instructions in the given ExecutableTree"""
        # TODO: look up the following reference to parse ANY PyWelkin file
        # https://code.activestate.com/recipes/578087-useful-unrestricted-grammar/
        raise NotImplementedError

    def interpret(self, input: str):
        tree = self.parser.parse(input)
        validation = self.validator.validate(tree)
        if not (validation):
            raise Exception
        self.run(tree)
