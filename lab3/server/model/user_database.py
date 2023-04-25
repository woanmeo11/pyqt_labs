class UserDatabase:
    def __init__(self):
        self.db = {}

    def login(self, username, password):
        return username in self.db and self.db[username] == password

    def register(self, username, password):
        if username not in self.db:
            self.db[username] = password
            return True
        else:
            return False
