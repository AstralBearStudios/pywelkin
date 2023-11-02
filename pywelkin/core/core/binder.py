# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from core.base import Recorder


class Interface:
    pass


# TODO: make this easy to work with OCAML and other programming languages. (Probably through Python's FFI)
class Binder:
    pass
    # Text : welkin.standard - { parsed-by-> Interface} -> welkin.attribute_tree - {binded-by-> Binder} -> Output : IO
