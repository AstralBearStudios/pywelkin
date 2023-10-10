# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0-WITH-LLVM-exception
# from lark import Lark
import lark


# TODO: make the path below applicable for any OS
def minimal_parse(input):
    """Parse"""

    minimal_path = "./grammars/minimal.lark"

    parser = lark.Lark.open(minimal_path, parser="lalr")

    output = parser.parse(input)

    print(output.pretty())
