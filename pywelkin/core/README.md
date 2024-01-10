# pywelkin.core

This module provides the core logic behind Welkin. It features

- A parser for any unicode grammar (and other encodings)
- A recorder that stores any Parse Tree in a graph
- The printer for showing graphs

Dependencies are kept to a minimum. The following will not change, because of how well they are developed, and the
relatively short lifespan

- lark: parsing engine that includes Unicode and AST support builtin. Absolutely essential for standard and user created
  grammars

# Credits

- lark: Erez Sheran and All Contributors. All of the Github issues were quite insightful, and you all have made a
  fantastic package!

# License

Copyright (c) 2023 Oscar Bender-Stone and pywelkin.core contributors.

This subpackage is licensed under: SPDX-Apache-2.0-WITH-LLVM-exception.
