from APP.MapPy import Map, curr_map
from APP.BluetoothPy import bluetooth

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

from PyQt6.QtWidgets import QFileDialog


class LoadFileDialog(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('Windows_Templates_UI/LoadFileDialog.ui', self)

        self.parent = parent
        self.geo_map = None
        self.status_text = None

        self.cancel_btn.clicked.connect(self.close)
        self.open_btn.clicked.connect(self.open_file)
        self.open_current_btn.clicked.connect(self.open_current_file)
        self.push_file_btn.clicked.connect(self.push_file)

        self.update()

    def update(self):
        if self.status_text is None:
            self.status_label.clear()
            self.status_label.hide()
        else:
            self.status_label.setText(self.status_text)
            self.status_label.show()
        self.status_text = None

        if self.geo_map is None:
            self.push_file_btn.hide()
            self.info_widget.hide()
            self.name_label.hide()
        else:
            self.push_file_btn.show()
            self.info_widget.show()
            self.name_label.show()

            self.update_info()

    def update_info(self):
        if self.geo_map.name is None:
            self.name_label.setText("Без имени")
        else:
            self.name_label.setText(self.geo_map.name)

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self, "Выбрать карту", '')
        if ok:
            with open(filename, mode='r', encoding='utf-8') as file:
                map_text = file.read()
                self.geo_map = Map(map_text, filename)

            if self.geo_map.type != "edit":
                self.geo_map = None
                self.status_text = "Неверный тип карты!!"

            self.update()

    def open_current_file(self):
        if curr_map.type != "edit":
            self.geo_map = None
            self.status_text = "Неверный тип карты!!"
        else:
            self.geo_map = curr_map

        self.update()

    def push_file(self):
        if bluetooth.is_connected():
            if bluetooth.push_file():
                self.parent.update()
                self.close()
            else:
                self.status_text = "Не удалось отправить инструкцию"
                self.update()
        else:
            self.parent.status_text = "Не удалось отправить инструкцию - нет подключения к Bluetooth!!"
            self.parent.update()
            self.close()