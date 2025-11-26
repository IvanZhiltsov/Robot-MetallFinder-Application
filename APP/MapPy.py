import json

save_key = "Ymap js for Robot-MetalFinder Application"


class Map:
    def __init__(self, map_js=None, name=None):
        if map_js is None:
            self.name = name
            self.type = "empty"
            self.data = None
        else:
            if not self.set_map(map_js, name):
                self.name = name
                self.type = "other"
                self.data = None

    def set_map(self, map_js, name=None):
        try:
            new_map = json.loads(map_js)
            key, new_type, new_data = new_map.values()

            if key != save_key:
                return False

            self.name = name
            self.type = new_type
            self.data = new_data

        except Exception:
            return False

        return True

    def update(self, map_js):
        map_object = json.loads(map_js)
        self.type, self.data = map_object.values()

    def js_for_save(self):
        map_object = {"key": save_key, "type": self.type, "data": self.data}
        return json.dumps(map_object)

    def push_js_for_html(self):
        map_object = {"type": self.type, "data": self.data}
        return json.dumps(map_object)

    def get_js_from_html(self, map_js):
        map_object = json.loads(map_js)
        self.type = map_object["type"]
        self.data = map_object["data"]


curr_map = Map()
