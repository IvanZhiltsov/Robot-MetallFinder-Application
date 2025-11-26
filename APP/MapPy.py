import json

# python <--> js API
# data for 'empty': None
# data for 'edit': [[x1, y1], [x2, y2]...]
# data for 'data': {'polygon': [[x1, y1], [x2, y2]...], 'metal_places': [[x1, y1], [x2, y2]...]}


class Map:
    def __init__(self, map_text=None, name=None):
        if map_text is None:
            self.name = name
            self.type = "empty"
            self.data = None
        else:
            if not self.setMap(map_text, name):
                self.name = name
                self.type = "other"
                self.data = None

    def setMap(self, map_txt, name=None):
        if map_txt == "other":
            return False

        self.name = name
        self.type = map_txt.rstrip()
        self.data = map_txt
        return True

    def push_js_for_html(self):
        map_object = [self.type, self.data]
        return json.dumps(map_object)

    def get_js_from_html(self, data):
        map_object = json.loads(data)
        print(map_object)

curr_map = Map()
