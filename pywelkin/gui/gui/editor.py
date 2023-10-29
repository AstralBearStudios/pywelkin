# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: LPGL-3.0-or-later

from PySide6 import QtWidgets


class TextEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
