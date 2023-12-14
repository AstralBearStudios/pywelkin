# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
#

from PySide6.QtWidgets import QMainWindow

# TODO: subclass QMainWindow as needed


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.showMaximized()
        self.setWindowTitle("Welkin Studio")
