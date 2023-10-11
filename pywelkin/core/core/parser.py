# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0-WITH-LLVM-exception
import lark


# TODO: decide how to implement regex parsing for minimal grammar
# TODO: make the path below applicable for any OS
def minimal_parse(input):
    """Parses a file with the minimal Welkin grammar"""

    minimal_path = "./grammars/minimal.lark"

    parser = lark.Lark.open(minimal_path, parser="lalr")

    output = parser.parse(input)

    print(output.pretty())


# TODO: decide whether grammasr should be written in lark OR welkin config files
def bootstrap_parse():
    """Allows any (well-formed) Welkin config file to be a grammar."""
    raise NotImplementedError
