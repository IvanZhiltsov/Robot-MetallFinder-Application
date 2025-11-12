class Bluetooth:
    def __init__(self):
        self.connection = False
        # {"name": name, "device": devices[name]}
        self.current_device = None
        self.devices = {
            "Robot1 - Режим ожидания":  {"adress": "",
             "info": {"mode": "Режим ожидания", "current_power": 20, "search_info": None}},

            "Robot2 - Рабочий режим": {"adress": "",
             "info": {"mode": "Рабочий режим", "current_power": 90, "search_info": None}},

            "Robot3 - Окончил работу": {"adress": "",
             "info": {"mode":"Окончил работу", "current_power": 40,
                      "search_info": {"places": 2, "spent_time": 90, "spent_power": 60}}}
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

    def get_dev_names(self):
        return self.devices

    def get_info(self):
        if self.connection:
            ok = True
        else:
            ok = False
        return self.current_device, ok

    def get_map(self):
        map = {"name": "Карта 1", "type": "data", "data": "Данные карты"}
        if self.connection:
            ok = True
        else:
            ok = False
        return map, ok

    def clear(self):
        if self.connection:
            ok = True
        else:
            ok = False

        name = self.current_device["name"]
        self.devices[name]["info"]["mode"] = "Режим ожидания"
        self.devices[name]["info"][ "search_info"] = None
        self.current_device = {"name": name, "device": self.devices[name]}

        return ok
