class ActionsManager:
    def __init__(self):
        # {"action": str, "data": js}
        self.actions = []
        self.index = -1

    def update(self):
        self.actions = []
        self.index = -1

    def add_action(self, action, data):
        self.actions = self.actions[:self.index + 1]
        self.actions.append({"action": action, "data": data})
        self.index += 1
        return self.chack_ends()

    def undo(self):
        self.index -= 1
        return self.actions[self.index]["data"], self.chack_ends()

    def recover(self):
        self.index += 1
        return self.actions[self.index]["data"], self.chack_ends()

    def chack_ends(self):
        ends = {"undo": True, "recover": True}
        if self.index == 0:
            ends["undo"] = False
        if self.index == len(self.actions) - 1:
            ends["recover"] = False
        return ends


actions_manager = ActionsManager()
