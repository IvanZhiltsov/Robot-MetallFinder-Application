import sys

import Bluetooth

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

        self.map_type = "empty"
        self.is_conn = Bluetooth.is_connected()

        self.tab_robot = TabRobot(self)
        self.menu = Menu(self)
        self.tab_map = TabMap(self)

    def load_file(self):
        pass


class TabMap:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        map_type = self.p.map_type

        if map_type == "empty":
            self.p.edit_map_widget.show()
        elif map_type == "edit":
            self.p.edit_map_widget.show()
        else:
            self.p.edit_map_widget.hide()


class TabRobot:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        self.data = None
        self.dev_btn_group = QButtonGroup(self.p)

        self.p.update_dev_btn.clicked.connect(self.update_devices)

        self.p.discon_btn.clicked.connect(self.disconnection)
        self.p.get_data_btn.clicked.connect(self.get_robot_data)
        self.p.clear_btn.clicked.connect(self.clear_robot)
        self.p.load_btn.clicked.connect(self.p.load_file)

        self.update()

    def update(self):
        if self.p.is_conn:
            self.update_info()

            if self.data["device"]["info"]['mode'] in ("Окончил работу", "Рабочий режим"):
                self.p.get_data_btn.setEnabled(True)
                self.p.clear_btn.setEnabled(True)
            else:
                self.p.get_data_btn.setEnabled(False)
                self.p.clear_btn.setEnabled(False)

            self.p.edit_widget.show()
            self.p.info_widget.show()
            self.p.devices_widwet.hide()

        else:
            self.update_devices()

            self.p.edit_widget.hide()
            self.p.info_widget.hide()
            self.p.devices_widwet.show()

    def update_info(self):
        # {"name": str, "mode": str, "current_power": int %, "search_info": dict}
        self.data = Bluetooth.get_info()

        self.p.name_lable.setText(f"Имя робота: {self.data['name']}")

        info = self.data['device']['info']
        self.p.mode_label.setText(f"Режим робота: {info['mode']}")
        self.p.current_power_bar.setValue(info['current_power'])

        if info['mode'] == "Окончил работу":
            self.p.search_info_widget.show()

            # {"places": int, "spent_time": int minutes, "spent_power": int %}
            search_info = info['search_info']

            time = search_info['spent_time']
            hours = time // 60
            minutes = time % 60

            self.p.places_label.setText(f"Обнаружено мест с металлом: {str(search_info['places'])}")
            self.p.spent_time_lable.setText(f"Затраченное время: {str(hours)} ч. {str(minutes)} мин.")
            self.p.spent_power_bar.setValue(search_info['spent_power'])
        else:
            self.p.search_info_widget.hide()

    def update_devices(self):
        # {"name": srtr, "adress": str}
        names = Bluetooth.get_dev_names()

        for btn in self.dev_btn_group.buttons():
            self.dev_btn_group.removeButton(btn)
            self.p.devices_vl.removeWidget(btn)
            del btn

        for name in names:
            btn = QPushButton(name, self.p)
            btn.clicked.connect(self.get_connection)

            self.dev_btn_group.addButton(btn)
            self.p.devices_vl.addWidget(btn)

    def get_connection(self):
        name = self.p.sender().text()
        if Bluetooth.get_connection(name):
            self.p.is_conn = True
        else:
            self.p.is_conn = False
        self.update()

    def disconnection(self):
        Bluetooth.disconection()
        self.p.is_conn = False
        self.update()

    def get_robot_data(self):
        pass

    def clear_robot(self):
        pass


class Menu:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        self.p.action_open.triggered.connect(self.open_file)
        self.p.action_save.triggered.connect(self.save_file)
        self.p.action_save_as.triggered.connect(self.save_as_file)
        self.p.action_load.triggered.connect(self.p.load_file)

        if self.p.is_conn:
            self.p.action_load.setEnabled(True)
        else:
            self.p.action_load.setEnabled(False)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def save_as_file(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
