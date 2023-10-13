# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: LPGL-3.0-or-later
#
# October 11, 2023: This is currently test code for the gui framework. Please do NOT use this
# in production or immediate personal use. This has a long way to go before it can be used.

import sys
import splash, window
from PySide6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash.run_splash()
    app.processEvents()

# window.display()
window = QtWidgets.QMainWindow()
window.showMaximized()
window.setWindowTitle("Welkin Studio")
window.show()
sys.exit(app.exec())
