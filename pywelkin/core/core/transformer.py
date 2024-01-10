#!/usr/bin/env python3

from lark.visitors import Token, Transformer

from typing import Protocol


# class TerminalEncoder(Protocol):
#    @staticmethod
#    def float(self, number_string):
#        # Generalized float function that
#        # works for any encoding
#        # By default, uses Pythons' builtin float function
#        return float(number_string)


class SignatureTransformer(Transformer):
    """Supports terminal signatures:
    - Removes whitespace and keywords
    - Converts numbers into floats
    and strings into Python strings"""

    def WORD(self, token):
        return token.value

    def NUMBER(self, token: Token):
        return token.update(value=float(token))

    def STRING(self, token):
        (string,) = token
        contents = string[1:-1]
        return contents
