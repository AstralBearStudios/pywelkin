# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
# Creates the core data structure to hold and combine Welkin graphs

from typing import Any

# We want to store InformationTrees as graphs, possibly using an adjancey matrix representation.
# So we list all of the nodes, and then we have a matrix of their connections
# But do the names of the nodes matter? According to CFLT, no, not at all. If we make connections on their names, sure,
# but that would be recognized by the connections themselves!
# Probably helpful to look at semantics for this!
# Semantics: {} mean possibility -> continuum focus, connection means and -> focus continuum


class Fold:
    pass


class Focus:
    """Equality based data structure"""

    pass


class Continuum:
    """Difference based data structure"""

    pass


# A --> B
# B --> C
# To:
# 1 --> 2
# 2 --> 3
# 1 --> {A}
# 2 --> {B} lines 36-38 (connnecting each number to alias) are LABELS, a part of attributes!. They can be stored separately (or in different references/pointers)
# 3 --> {C}
# Adjaceny matrix is independent from aliases; this is an important part! Names do not change connections!
#
# TODO: determine the best way to handle defining the naturals. Without this, Welkin cannot define FOL!
# Naturals Von Neumann Style: 0 = {}, 1 = { {} }, 2 = {{}, {{}}}, ...
# We want to encode the dots with a loop. And we want to define what operators are in terms of base Welkin
# nat {
#   0
#   n -> { n' { n'  } }
# }
# nat - nat -> nat
#
