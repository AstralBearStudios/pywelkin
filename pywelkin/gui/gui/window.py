# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: LPGL-3.0-or-later
#
from PySide6 import QtWidgets


def display():
    """Displays the main window"""

    window = QtWidgets.QMainWindow()
    window.showMaximized()
    window.setWindowTitle("Welkin Studio")
    window.show()
