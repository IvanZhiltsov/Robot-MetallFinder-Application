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
            "data": '{"key": "Ymap js for Robot-MetalFinder Application", "type": "edit", "data": '
                    '{"polygonCords": '
                        '[[55.721527404303544, 37.6172212943081], [55.74942144391606, 37.58117240514797], '
                        '[55.77361879169219, 37.57464927282375], [55.78019786193889, 37.590442119503436], '
                        '[55.77594094384686, 37.61001151647607], [55.76800635034173, 37.618251262569835], '
                        '[55.76994176661509, 37.629580913448734], [55.777101967820926, 37.64091056432763], '
                        '[55.77768246678238, 37.6656298026089], [55.76703860601849, 37.68039268102685], '
                        '[55.758134226265966, 37.678676067257335], [55.73605804796461, 37.650866924190936]], '
                    '"finishCords": [55.76800635034173, 37.655330119991696], "metalCords": null}}'},

            "Robot3 - Окончил работу": {"adress": "",
            "info": {"mode":"Окончил работу", "current_power": 40,
                    "search_info": {"places": 2, "spent_time": 90, "spent_power": 60}},
            "data": '{"key": "Ymap js for Robot-MetalFinder Application", "type": "data", "data": '
                    '{"polygonCords": '
                        '[[55.73466828792217, 37.595118700018496], [55.745030532371935, 37.583102403631784], '
                        '[55.761391440011295, 37.58653563117084], [55.77155303023619, 37.6035301074892], '
                        '[55.77232713759227, 37.63013762091695], [55.768940303926, 37.647132097235286], '
                        '[55.75984277367772, 37.65743177985249], [55.74696709400034, 37.65846174811421], '
                        '[55.739801333803385, 37.657088457098595], [55.735539985010476, 37.65176695441305], '
                        '[55.73069697601227, 37.639064012518496], [55.7290502154933, 37.622241197577104], '
                        '[55.730018906599646, 37.60782164191304]], '
                    '"finishCords": null, '
                    '"metalCords":'
                        '[[55.74687026821147, 37.6313392505556], [55.74687026821147, 37.6313392505556], '
                        '[55.74687026821147, 37.6313392505556], [55.74725756991911, 37.608508287420854], '
                        '[55.74725756991911, 37.608508287420854], [55.74725756991911, 37.608508287420854], '
                        '[55.76052032279867, 37.620867906561486], [55.76052032279867, 37.620867906561486], '
                        '[55.76052032279867, 37.620867906561486]]}}'}
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
