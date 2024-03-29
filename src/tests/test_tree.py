#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Make sure overarching tree properties work; see lark/tests/test_tree.py

from pywelkin.containers import Tree


def test_operations():
    tree = Tree("A")
    tree["B", "C"] = "D"
    print(tree)
