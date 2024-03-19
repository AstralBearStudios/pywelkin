#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception

import pytest
from typing import List
from pywelkin import Base

base: Base = Base(strict=True)

# Main goals:
# Test that parser + transformer works

# Possible user inputs
# Fairly random for wider test coverage
user_inputs = {
    # Basic tests with only one or two levels of nesting
    # All vertex names are intentionaljy abstract
    # "B, A.B.C { B, C { D, E { F, G, H } } }"
    "{ A --> C }"
    # "{ A.C.D.E.F, B ,},"
    # "_{ A, B, C, D, E G, H --> D }"
    # "A := B, D --> B --> C"
    # "A --> B --> C --> D",
    # "A { D := B { C } }"
    # "_{ A.B  C := D  D --> _{ 'Text' }}",
    # "_{ A <-- _{ B C }}",
    # "_{ ...A.B#0.3, C#1 -- B#2 }",
    # "_{ B --> D  A.B --> C}"
    # More involved examples that mirror quick notes
    # "house { family { mom dad me } pets { dog cat } }"
    # """story {
    #     'Tortoise and the Hare'
    #     characters {
    #         T := Tortoise,
    #         H := Hare
    #     }
    #     plot {
    #         characters.T  - beats -> characters.H
    #     }
    # } """,
    # " ",
    # " ",
}


@pytest.mark.parametrize("user_input", user_inputs)
class TestBase:
    """Test functionality for Base Welkin, specifically with:
    - Parsing
    - Recording
    """

    user_inputs: List[str]

    def test_user_input_trees(self, user_input):  # , user_inputs):
        print(base.parser.parse(user_input))
        # for text in user_inputs:

    # def test_user_input_graphs(self):
    #     return False
    # def test_input_encoding(self):
    #     return False
