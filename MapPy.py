class Map:
    def __init__(self):
        self.name = None
        self.type = "empty"
        self.data = None

    def setMap(self, name, map_txt):
        self.name = name
        self.type = "data"
        self.data = map_txt
