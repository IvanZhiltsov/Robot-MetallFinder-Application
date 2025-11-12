connection = False
# {"name": name, "device": devices[name]}
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


def is_bluetooth():
    return True

def get_dev_names():
    global devices
    return devices

def is_connected():
    global connection
    return connection

def get_connection(name):
    global connection, current_device
    connection = True
    current_device = {"name": name, "device": devices[name]}
    return True

def disconection():
    global connection, current_device
    connection = False
    current_device = None
    pass

def get_info():
    global connection, current_device
    if connection:
        ok = True
    else:
        ok = False
    return current_device, ok

def get_map():
    global connection

    map = {"name": "Карта 1", "type": "data", "data": "Данные карты"}
    if connection:
        ok = True
    else:
        ok = False
    return map, ok

def clear():
    global devices, current_device

    if connection:
        ok = True
    else:
        ok = False

    name = current_device["name"]
    devices[name]["info"]["mode"] = "Режим ожидания"
    devices[name]["info"][ "search_info"] = None
    current_device = {"name": name, "device": devices[name]}

    return ok
