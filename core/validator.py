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


# class Validator(SemanticsValidator):
#     @staticmethod
#     def check_name_collisions(self, contents):
#         # Check for name collisons
#         # TODO: make sure contents is always hashable (check connector)
#         contents_set = set(contents)
#         if len(contents) != len(contents_set):
#             raise SyntaxError("Name collision")
#             # raise SyntaxError
#         # for item in contents:
#         #     # print("Input:", input, "\n")
#         #     unique_label = item
#         #     # Check for name collison
#         #     if unique_ident == current_label and unique_label:
#         #         print("Current syntax error")
#         #         #raise SyntaxError
#         #     current_ident = unique_ident
#
#     @staticmethod
#     def check_relative_member(self, contents):
#         return False
