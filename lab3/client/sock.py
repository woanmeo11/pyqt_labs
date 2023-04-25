import json
import socket


class Sock:
    def __init__(self, host="localhost", port=4444):
        self.session_id = ""
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.conn.connect((self.host, self.port))

    def send(self, obj):
        if self.session_id:
            obj["session_id"] = self.session_id
        self.conn.sendall(json.dumps(obj).encode())

    def recv(self, size=1024):
        res = self.conn.recv(size)
        return json.loads(res) if res else {}
