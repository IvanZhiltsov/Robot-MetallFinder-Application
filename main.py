import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import QtCore, QtWidgets

from PyQt6.QtWidgets import QPushButton, QButtonGroup

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)

        self.is_conn = False
        self.dev_btn_group = QButtonGroup(self)

        self.init_tab_map()
        self.init_tab_robot()
        self.init_menu()

    # map_type: "empty", "edit", "data"
    def init_tab_map(self, map_type="empty", data=None):
        if map_type == "empty":
            self.edit_map_widget.show()
        elif map_type == "edit":
            self.edit_map_widget.show()
        else:
            self.edit_map_widget.hide()

    def init_tab_robot(self):
        if self.is_conn:
            self.connection_widget.show()
            self.status_widget.show()
            self.devices_widwet.hide()

        else:
            self.update_devices()

            self.update_dev_btn.clicked.connect(self.update_devices)

            self.connection_widget.hide()
            self.status_widget.hide()
            self.devices_widwet.show()

    def update_devices(self):
        # {"name": '', "adress": ''}
        devices = [{"name": "Robot1", "adress": ""},
                   {"name": "Наушники", "adress": ""},
                   {"name": "Колонка", "adress": ""}]

        for btn in self.dev_btn_group.buttons():
            self.dev_btn_group.removeButton(btn)
            self.devices_vl.removeWidget(btn)

        for device in devices:
            name = device["name"]
            btn = QPushButton(name, self)
            self.dev_btn_group.addButton(btn)
            self.devices_vl.addWidget(btn)
        self.dev_btn_group.buttonClicked.connect(self.get_connection)

    def get_connection(self):
        pass

    def init_menu(self):
        # map_test_lable
        self.action_open.triggered.connect(self.open_file)
        self.action_save.triggered.connect(self.save_file)
        self.action_save_as.triggered.connect(self.save_as_file)
        self.action_load.triggered.connect(self.load_file)

        if self.is_conn:
            self.action_load.setEnabled(True)
        else:
            self.action_load.setEnabled(False)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def save_as_file(self):
        pass

    def load_file(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
