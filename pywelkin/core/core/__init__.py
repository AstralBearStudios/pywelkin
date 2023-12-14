# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Roadmap (version 0.3.0):
# - Finalize the Parser class
# - Finalize base and standard Welkin
#   - Incorporate these into the standard itself
# - Implement the InformationTree and ExecutableTree classes
#   - Connect the implementation of both into CFLT
# - Ensure that the interpreter is Turing complete
# - Ensure that the interpreter allows custom parsers to be made with, e.g., custom char*
#   - Mainly ensure that char* works for ascii, unicode. (Plugins can be made for esoteric languages)
# - Figure out how to best bootstrap new features (e.g., direct interface to the operating system)


from .standard import Interpreter
from .base import Recorder

from .parser import Parser

__all__ = ["Parser", "Interpreter", "Recorder"]
