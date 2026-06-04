class Memory:
    def __init__(self):
        self.history = []

    def add(self, role, msg):
        """Appends a new conversation interaction turn to the logs."""
        self.history.append({"role": role, "msg": msg})

    def get(self):
        """Returns the full conversation history from the logs."""
        return self.history