current_device = {}


def get_devices():
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
    mode = "Окончил работу"
    search_info = None
    if mode == "Окончил работу":
        # {"places": int, "spent_time": int minutes, "spent_power": int %}
        search_info = {"places": 2, "spent_time": 90, "spent_power": 80}
    return {"name": current_device["name"], "mode": "Окончил работу", "current_power": 20, "search_info": search_info}
