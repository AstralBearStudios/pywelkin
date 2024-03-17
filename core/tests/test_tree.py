#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

# Make sure overarrching tree properties work; see lark/tests/test_tree.py

from lib.core import Tree


def test_operations():
    tree = Tree("A")
    tree["B", "C"] = "D"
    print(tree)
