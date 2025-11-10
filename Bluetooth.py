current_device = {}


def get_devices():
    # {"name": '', "adress": ''}
    devices = [{"name": "Robot1", "adress": ""},
               {"name": "Наушники", "adress": ""},
               {"name": "Колонка", "adress": ""}]
    return devices

def is_connected():
    return False

def get_connection(device):
    global current_device
    current_device = device
    return True

def get_info():
    return {"name": current_device["name"], "mode": 'Окончил работу', "current_power": 80}
