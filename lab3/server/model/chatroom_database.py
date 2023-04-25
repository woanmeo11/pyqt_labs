import random
from string import ascii_letters, digits


class ChatroomDatabase:
    def __init__(self):
        self.db = {}

    def get_room(self, room_id):
        return self.db[room_id]

    def new_room(self):
        while True:
            room_id = "".join(random.choices(digits + ascii_letters, k=6))

            if room_id in self.db:
                continue

            self.db[room_id] = []
            return room_id

    def join_room(self, room_id, session_id):
        if room_id not in self.db:
            return False

        self.db[room_id].append(session_id)
        return True

    def remove_from_room(self, room_id, session_id):
        if room_id not in self.db:
            return False

        self.db[room_id].remove(session_id)
        return True
