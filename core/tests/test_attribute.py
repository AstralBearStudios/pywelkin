#  Spdx-FileCopyrightText: Oscar Bende-Stone <oscarbenderstone@gmail.com>
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM Exception


from lib.core import Attributor

attributor = Attributor(strict=True)
class TestAttribute:
    def test_graph(self):
        assert False



    # Expected parse: Graph[A], Graph[Connection[A, B]], Graph[Connection[A, B], Connection[B, C], Connection[D, E]]


    def test_input_trees(self):
        inputs = [
            # Basic tests with only one or two levels of nesting
            # '_{ B A _{ "Description about A" }}',
            # '{ 2 3 A { "Description about A" }}',
            # "{ A --> {B C} D D {} }",
            # "{ A -- B -- C  D -- E }",
            # More involved examples that mirror quick notes
            # "_{ 42, -- .#4.2.B, }",
            "_{ * --> * }"
        ]
        for input in inputs:
            print(attributor.parser.parse(input))

    test_input_trees()
