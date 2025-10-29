import sys

from PyQt6.QtWebEngineWidgets import QWebEngineView

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore, QtWidgets


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

yandex_map_html = QtCore.QUrl("https://yandex.ru/maps/213/moscow/?ll=37.586333%2C55.772715&source=serp_navig&z=10")


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(30, 30, 1500, 800)

        self.map = QWebEngineView(self)
        self.map.resize(1500, 800)
        self.map.load(yandex_map_html)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
