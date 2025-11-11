current_device = None
devices = {
    "Robot1 - Режим ожидания":  {"adress": "",
     "info": {"mode": "Режим ожидания", "current_power": 20, "search_info": None}},

    "Robot2 - Рабочий режим": {"adress": "",
     "info": {"mode": "Рабочий режим", "current_power": 90, "search_info": None}},

    "Robot3 - Окончил работу": {"adress": "",
     "info": {"mode":"Окончил работу", "current_power": 40,
              "search_info": {"places": 2, "spent_time": 90, "spent_power": 60}}}
    }


def get_dev_names():
    global devices
    return devices

def is_connected():
    return False

def get_connection(name):
    global current_device
    current_device = {"name": name, "device": devices[name]}
    return True

def get_info():
    return current_device

def disconection():
    pass
