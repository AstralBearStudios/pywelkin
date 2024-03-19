#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# TODO: separate pywelkin from welkin error handling
# Only error handling in welkin: Validator
# All else: put into @system!

from .graph import Label


class LocatedError(SyntaxError):
    descriptor: str

    def __str__(self):
        context, line, column = self.args
        return f"{self.descriptor} at line {line}, column {column}"


class NameCollisionError(LocatedError):
    """Raised if any unit is repeated twice.
    This is the only error raised for Base Welkin"""

    label: Label
    descriptor = "Repeated unit, connection, or alias"

    def __init__(self, unit):
        self.unit = unit
        super(NameCollisionError, self).__init__()


class SelfAliasError(LocatedError):
    """Raised if a unit is used as its own alias.
    A unit does not need to be its own alias."""

    descriptor = "Unit used as its own alias"


class ArgumentError(LocatedError):
    """Raised if wrong number of arguments given in an attribute"""

    received: int
    expected: int
    descriptor: str

    def __init__(self, received, expected):
        (self.received, self.expected) = (received, expected)
        self.descriptor = (
            f"Got {self.received} arguments, expected {self.expected} arguments"
        )
        super(LocatedError, self).__init__()


class Validator:
    pass
