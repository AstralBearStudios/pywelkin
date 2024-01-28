# SPDX-FileCopyrightText: 2023 Oscar Bender-Stone <oscarbenderstone@gmail.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# October 12, 2023: This is currently test code for the gui framework. Please do NOT use this
# in production or immediate personal use. This has a long way to go before it can be used.

from PySide6 import QtGui, QtWidgets

import time


def run_splash():
    """Run the main splash screen."""
    pixmap = QtGui.QPixmap()
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()

    # Artificailly simulates possible loading for app
    time.sleep(1)
