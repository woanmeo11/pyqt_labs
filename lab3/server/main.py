import json
import socket
import threading

from model.chatroom_database import ChatroomDatabase
from model.user_database import UserDatabase
from routes import (
    SESSION,
    disconnect_user,
    join_room,
    login,
    logout,
    new_room,
    out_room,
    register,
    res,
    send_msg,
)


def handler(conn, addr):
    print(f"New connection from: {addr}")

    session_id = ""

    while True:
        req = conn.recv(1024)

        # Disconnected
        if not req:
            if session_id:
                disconnect_user(roomdb, session_id)
            break

        print(req.decode())

        try:
            req = json.loads(req)
        except:
            res(conn, "Invalid body structre!")
            continue

        if "action" not in req:
            res(conn, "Missing action!")
            continue

        action = req["action"]

        if "session_id" in req:
            if req["session_id"] not in SESSION:
                res(conn, "Missing session_id!")
                continue

            session_id = req["session_id"]

            if action == "new_room":
                new_room(roomdb, conn, req)
            elif action == "join_room":
                join_room(roomdb, conn, req)
            elif action == "send_msg":
                send_msg(roomdb, req)
            elif action == "out_room":
                out_room(roomdb, conn, req)
            elif action == "logout":
                session_id = ""
                logout(roomdb, conn, req)
            else:
                res(conn, "Invalid action!")
        else:
            if action == "register":
                register(userdb, conn, req)
            elif action == "login":
                session_id = login(userdb, conn, req)
            else:
                res(conn, "Invalid action!")


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444

    userdb = UserDatabase()
    roomdb = ChatroomDatabase()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            threading.Thread(
                target=handler,
                args=(
                    conn,
                    addr,
                ),
            ).start()
