️⚠ **Warning: This repository is a WIP. This project is in its early stages and is not in its alpha release. Please wait to submit any issues, and stay tuned for updates.**

**Update March 13, 2024: as a late edition to the February update in [Welkin](https://github.com/astral-bear/welkin), the scope of this project is being significantly reduced. PyWelkin will only be a core library. It does provide more support beyond the standard, but it does require some concepts from the Vero spec (TBD).**

Welcome to PyWelkin, the official python implementation of [Welkin](https://github.com/astral-bear/welkin). This is a library for:
- Parsing Welkin and any Context Free Grammar
- Storing Information Graphs in memory and on disk 
- Generating canonical strings

Analyzing graphs in python will be a separate extension (TBD).

Many projects for AstralBearStudios will be bootstrapped using pywelkin. These include:
- Vero (Finitary Mathematical Basis): TBD
- Grove (Welkin Package Manager): TBD
- Pruvi (Unified Proof Assistant): TBD
- Stratus (Assembly + OS Spec): TBD


Dependencies are kept to a minimum. The following will not change, because of how well they are developed, and the
relatively short lifespan of pywelkin.

- lark: parsing engine that includes Unicode and AST support builtin. Absolutely essential for Welkin and custom 
  grammars.

# Credits

- lark: Erez Sheran and All Contributors. All of the Github issues were quite insightful, and you all have made a fantastic package!


# Installation
  - Pip: TBD
  - Poetry: clone the repository first.
  ```bash
    git clone https://github.com/AstralBearStudios/pywelkin
  ```

    Then install with poetry.

  ```bash
    cd pywelkin && poetry install
  ```

# License
  Copyright (c) 2023, Oscar Bender-Stone and the PyWelkin contributors.

  This package is licensed under: SPDX-Apache-2.0-WITH-LLVM-exception.
