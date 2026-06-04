class ChatMemory:
    def __init__(self, limit=10):
        self.limit = limit
        self.history = []

    def add_user(self, msg):
        self.history.append(("human", msg))
        self._trim()

    def add_ai(self, msg):
        self.history.append(("ai", msg))
        self._trim()

    def get(self):
        return self.history

    def clear(self):
        self.history = []

    def _trim(self):
        # FIX: Added a colon ':' to properly slice and keep the last N items as a list
        if len(self.history) > self.limit * 2:
            self.history = self.history[-(self.limit * 2):]              
