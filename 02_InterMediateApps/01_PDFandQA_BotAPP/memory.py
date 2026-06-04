class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, msg):
        self.history.append({"role": role, "msg": msg})

    def get(self):
        return self.history[-10:]
