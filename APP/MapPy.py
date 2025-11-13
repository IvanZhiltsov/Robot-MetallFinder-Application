class Map:
    def __init__(self, map_text=None, name=None):
        if map_text is None:
            self.name = name
            self.type = "empty"
            self.data = None
        else:
            self.setMap(map_text, name)

    def setMap(self, map_txt, name=None):
        self.name = name
        self.type = map_txt.rstrip()
        self.data = map_txt

curr_map = Map()
