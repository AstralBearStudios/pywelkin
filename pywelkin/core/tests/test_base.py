# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception


from core.base import Recorder

# Expected parse: Graph[A], Graph[Connection[A, B]], Graph[Connection[A, B], Connection[B, C], Connection[D, E]]

recorder = Recorder(strict=True)


def test_input_trees():
    inputs = [
        '{ 2, 3, A { "Description about A" }}',
        "{ A --> {B C} D D {} }",
        "{ A -- B -- C  D -- E }",
    ]
    for input in inputs:
        print(recorder.parser.parse(input))


test_input_trees()
(
