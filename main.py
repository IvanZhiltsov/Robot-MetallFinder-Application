import sys

import BluetoothPy

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

        self.is_conn = Bluetooth.is_connected()
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
        self.update_dev_btn.clicked.connect(self.update_devices)

        self.discon_btn.clicked.connect(self.disconnection)
        self.get_data_btn.clicked.connect(self.get_robot_data)
        self.clear_btn.clicked.connect(self.clear_robot)
        self.load_btn.clicked.connect(self.load_file)

        self.update_tab_robot()

    def update_tab_robot(self):
        if self.is_conn:
            self.update_info()

            self.edit_widget.show()
            self.info_widget.show()
            self.devices_widwet.hide()

        else:
            self.update_devices()

            self.edit_widget.hide()
            self.info_widget.hide()
            self.devices_widwet.show()

    def update_info(self):
        # {"name": str, "mode": str, "current_power": int %, "search_info": dict}
        data = Bluetooth.get_info()

        self.name_lable.setText(f"Имя робота: {data['name']}")
        self.mode_label.setText(f"Режим робота: {data['mode']}")
        self.current_power_bar.setValue(data['current_power'])

        if data['mode'] == "Окончил работу":
            self.search_info_widget.show()

            # {"places": int, "spent_time": int minutes, "spent_power": int %}
            info = data['search_info']

            time = info['spent_time']
            hours = time // 60
            minutes = time % 60

            self.places_label.setText(f"Обнаружено мест с металлом: {str(info['places'])}")
            self.spent_time_lable.setText(f"Затраченное время: {str(hours)} ч. {str(minutes)} мин.")
            self.spent_power_bar.setValue(info['spent_power'])
        else:
            self.search_info_widget.hide()

    def update_devices(self):
        # {"name": srtr, "adress": str}
        devices = Bluetooth.get_devices()
        self.dict_btn_dev = {}

        for btn in self.dev_btn_group.buttons():
            self.dev_btn_group.removeButton(btn)
            self.devices_vl.removeWidget(btn)
            del btn

        for device in devices:
            name = device["name"]
            btn = QPushButton(name, self)
            btn.clicked.connect(self.get_connection)

            self.dev_btn_group.addButton(btn)
            self.devices_vl.addWidget(btn)

            self.dict_btn_dev[btn] = device

    def get_connection(self):
        device = self.dict_btn_dev[self.sender()]
        if Bluetooth.get_connection(device):
            self.is_conn = True
        else:
            self.is_conn = False
        self.update_tab_robot()

    def disconnection(self):
        pass

    def get_robot_data(self):
        pass

    def clear_robot(self):
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
