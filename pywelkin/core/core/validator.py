#  SPDX-FileCopyrightText: 2024 Oscar Bender-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

# from exceptions import TODO
from typing import Protocol


class Validator(Protocol):
    def exception(self):
        raise NotImplementedError


class SyntaxValidator(Validator, Protocol):
    def exception(self):
        raise NotImplementedError


class SemanticsValidator(Validator, Protocol):
    def exception(self):
        raise NotImplementedError


# TODO: figure out better name!
class ErrorHandler(Validator, Protocol):
    """Error handling during parsing"""

    errors: dict[str, str]

    def run(self, error) -> bool:
        """Runs the error handler on an individual token and checks how to respond to error"""
        raise NotImplementedError
