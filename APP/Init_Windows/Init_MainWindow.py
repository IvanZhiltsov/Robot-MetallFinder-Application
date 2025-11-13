from APP.Init_Windows.Init_LoadFileDialog import LoadFileDialog

from APP.MapPy import Map, curr_map
from APP.BluetoothPy import bluetooth

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import QtCore

from PyQt6.QtWidgets import QPushButton, QButtonGroup, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows_Templates_UI/MainWindow.ui', self)

        self.tabWidget.setCurrentIndex(0)

        self.tab_robot = TabRobot(self)
        self.tab_map = TabMap(self)
        self.menu = Menu(self)

        self.load_file_dialog = None

        self.status_text = None

    def update(self):
        self.tab_robot.update()
        self.tab_map.update()
        self.menu.update()

        if self.status_text is None:
            self.statusBar().clearMessage()
        else:
            self.statusBar().showMessage(self.status_text)
        self.status_text = None

        if curr_map.name is not None:
            self.setWindowTitle(f"Robot-MetallFinder connector - [{curr_map.name}]")
        else:
            self.setWindowTitle(f"Robot-MetallFinder connector")

    def load_file(self):
        self.load_file_dialog = LoadFileDialog(self)
        self.load_file_dialog.show()


class TabMap:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        self.p.undo_btn.clicked.connect(self.undo)
        self.p.recover_btn.clicked.connect(self.recover)
        self.p.cursor_btn.clicked.connect(self.mode_cursor)
        self.p.poligon_btn.clicked.connect(self.draw_poligon)
        self.p.del_poligon_btn.clicked.connect(self.del_poligon)
        self.p.finish_btn.clicked.connect(self.create_finish)

        map_html = QtCore.QUrl("https://yandex.ru/maps/213/moscow/?ll=37.586333%2C55.772715&source=serp_navig&z=10")
        self.map_view = QWebEngineView(self.p.map_widget)
        self.p.map_layout.addWidget(self.map_view)
        self.map_view.load(map_html)

        self.update()

    def update(self):
        if curr_map.type in ("empty", "edit"):
            self.p.edit_map_widget.show()
        else:
            self.p.edit_map_widget.hide()

    def undo(self):
        pass

    def recover(self):
        pass

    def mode_cursor(self):
        pass

    def draw_poligon(self):
        pass

    def del_poligon(self):
        pass

    def create_finish(self):
        pass


class TabRobot:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        self.dev_btn_group = QButtonGroup(self.p)
        self.p.update_dev_btn.clicked.connect(self.update)

        self.p.discon_btn.clicked.connect(self.disconnection)
        self.p.get_data_btn.clicked.connect(self.get_robot_data)
        self.p.clear_btn.clicked.connect(self.clear_robot)
        self.p.load_btn.clicked.connect(self.p.load_file)

        self.update()

    def update(self):
        if bluetooth.is_bluetooth():
            self.p.is_bluetooth_lable.clear()
        else:
            self.p.is_bluetooth_lable.setText("Нет подключения к Bluetooth!!")

        if bluetooth.is_connected():
            self.update_info()

            self.p.edit_widget.show()
            self.p.info_widget.show()
            self.p.devices_widwet.hide()

        else:
            self.update_devices()

            self.p.edit_widget.hide()
            self.p.info_widget.hide()
            self.p.devices_widwet.show()

    def update_info(self):
        # {"name": str, "device": {"adress": str, "info": dict}}
        data, ok = bluetooth.get_info()

        if not ok:
            self.p.statusBar().showMessange("Не удалось получить информацию о роботе")

            self.p.info_widget.hide()

            self.p.get_data_btn.setEnabled(False)
            self.p.clear_btn.setEnabled(False)
            self.p.load_btn.setEnabled(False)

        else:
            self.p.load_btn.setEnabled(True)

            self.p.name_lable.setText(f"Имя робота: {data['name']}")

            # {"mode": str, "current_power": int %, "search_info": dict}
            info = data['device']['info']
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

            if info['mode'] in ("Окончил работу", "Рабочий режим"):
                self.p.get_data_btn.setEnabled(True)
                self.p.clear_btn.setEnabled(True)
            else:
                self.p.get_data_btn.setEnabled(False)
                self.p.clear_btn.setEnabled(False)

    def update_devices(self):
        for btn in self.dev_btn_group.buttons():
            self.dev_btn_group.removeButton(btn)
            self.p.devices_vl.removeWidget(btn)
            del btn

        names = bluetooth.get_dev_names()

        if len(names) == 0:
            self.p.divices_label.setText("Не найдены устройства для подключения")
        else:
            self.p.divices_label.setText("Доступные устройства:")

            for name in names:
                btn = QPushButton(name, self.p)
                btn.clicked.connect(self.get_connection)

                self.dev_btn_group.addButton(btn)
                self.p.devices_vl.addWidget(btn)

    def get_connection(self):
        name = self.p.sender().text()
        bluetooth.get_connection(name)
        if not bluetooth.is_connected():
            self.p.status_text = f"Не удалось подключиться к устройству {name}"
        self.p.update()

    def disconnection(self):
        bluetooth.disconection()
        self.p.update()

    def get_robot_data(self):
        # {"name": str, "map_text": str}
        geo_map, ok = bluetooth.get_map()
        if not ok:
            self.p.status_text = "Не удалось получить карту"
        else:
            curr_map.setMap(*geo_map)
        self.p.update()

    def clear_robot(self):
        ok = bluetooth.clear()
        if not ok:
            self.p.status_text = "Не удалось очистить память"
        self.update()


class Menu:
    def __init__(self, parent):
        super().__init__()
        self.p = parent

        self.p.action_open.triggered.connect(self.open_file)
        self.p.action_save.triggered.connect(self.save_file)
        self.p.action_save_as.triggered.connect(self.save_as_file)
        self.p.action_load.triggered.connect(self.load_file)

        self.update()

    def update(self):
        if bluetooth.is_connected() and curr_map.type == "edit":
            self.p.action_load.setEnabled(True)
        else:
            self.p.action_load.setEnabled(False)

    def open_file(self):
        filename, ok = QFileDialog.getOpenFileName(self.p, "Открыть файл", '')
        if ok:
            with open(filename, mode='r', encoding='utf-8') as file:
                map_text = file.read()
                if not curr_map.setMap(map_text, filename):
                    self.p.status_text = "Не удалось открыть файл неизвестного типа"
            self.p.update()

    def save_file(self):
        pass

    def save_as_file(self):
        pass

    def load_file(self):
        self.p.load_file()
        self.p.load_file_dialog.open_current_file()