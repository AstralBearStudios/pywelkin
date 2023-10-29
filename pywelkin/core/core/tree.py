# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from typing import Self, List, Union, Tuple


class InformationTree:
    """The Welkin Information Graph (WIG) data structure that can be stored and traversed. This does NOT contain any
    additional instructions on how to traverse the tree. For direct execution, see interpreter.ExecutableTree
    """

    node: List[Self]
    pass


class ExecutableTree(InformationTree):
    """An InformationTree that contains valid instructions for the interpreter"""
