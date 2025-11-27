from PyQt6 import QtBluetooth as QtBt

real_devices = []
real_count_devices = 0
stop_count_devices = 5


class ScanDevices(QtBt.QBluetoothDeviceDiscoveryAgent):
    def __init__(self, count, parent):
        super().__init__(parent)

        self.parent = parent
        self.stop_count = count
        self.count_devices = 0

        self.deviceDiscovered.connect(self.get_device)

        self.start()

    def get_device(self, device):
        name = device.name()
        real_devices.append(name)

        self.count_devices += 1

        if self.count_devices >= self.stop_count:
            self.stop()
            self.parent.exec()


class Bluetooth:
    def __init__(self):
        self.connection = False

        # {"name": name, "device": devices[name]}
        self.current_device = None

        self.devices = {
            "Robot1 - Режим ожидания":  {"adress": "",
            "info": {"mode": "Режим ожидания", "current_power": 20, "search_info": None},
            "data": None},

            "Robot2 - Рабочий режим": {"adress": "",
            "info": {"mode": "Рабочий режим", "current_power": 90, "search_info": None},
            "data": None},

            "Robot3 - Окончил работу": {"adress": "",
            "info": {"mode":"Окончил работу", "current_power": 40,
                    "search_info": {"places": 2, "spent_time": 90, "spent_power": 60}},
            "data": None}
           }

    def is_bluetooth(self):
        return True

    def is_connected(self):
        return self.connection

    def get_connection(self, name):
        self.connection = True
        self.current_device = {"name": name, "device": self.devices[name]}
        return True

    def disconection(self):
        self.connection = False
        self.current_device = None
        pass

    def get_dev_names(self, bl_app):
        global real_devices, stop_count_devices

        ScanDevices(stop_count_devices, bl_app)

        new_real_dev = real_devices
        real_devices = []

        all_dev = [self.devices, new_real_dev]
        return all_dev

    def get_info(self):
        if self.connection:
            ok = True
        else:
            ok = False
        return self.current_device, ok

    def get_map(self):
        map_js = self.current_device["device"]["data"]
        if self.connection:
            ok = True
        else:
            ok = False
        return map_js, ok

    def clear(self):
        if self.connection:
            ok = True
        else:
            ok = False

        name = self.current_device["name"]
        self.devices[name]["info"]["mode"] = "Режим ожидания"
        self.devices[name]["info"][ "search_info"] = None
        self.devices[name]["data"] = None
        self.current_device = {"name": name, "device": self.devices[name]}

        return ok

    def push_file(self, map_js):
        if self.connection:
            ok = True
        else:
            ok = False

        name = self.current_device["name"]
        self.devices[name]["info"]["mode"] = "Рабочий режим"
        self.devices[name]["info"][ "search_info"] = None
        self.devices[name]["data"] = map_js
        self.current_device = {"name": name, "device": self.devices[name]}
        return ok


bluetooth = Bluetooth()
