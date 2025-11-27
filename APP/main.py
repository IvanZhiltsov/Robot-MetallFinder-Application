import sys

from BluetoothPy import bluetooth
from Init_Windows import Init_MainWindow

from PyQt6.QtWidgets import QApplication
from PyQt6 import QtCore, QtWidgets

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    Init_MainWindow.w_bluetooth = bluetooth
    Init_MainWindow.bl_app = app

    ex = Init_MainWindow.MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
