# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0-WITH-LLVM-exception


from core.parser import minimal_parse

minimal_parse("{ A }")
# AST Expected (node types only): start term graph term ident
