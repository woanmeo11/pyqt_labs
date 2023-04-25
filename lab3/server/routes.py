import json
import re
from uuid import uuid4

from model.chatroom_database import ChatroomDatabase
from model.user_database import UserDatabase

SESSION = {}


def broadcast(db, room_id, session_id, msg):
    members = db.get_room(room_id)
    for member_id in members:
        if member_id != session_id:
            res(SESSION[member_id]["conn"], msg, "send_msg")


def res(conn, msg="", action="", session_id="", room_id=""):
    obj = {
        "action": action,
        "msg": msg,
        "session_id": session_id,
        "room_id": room_id,
    }
    response = {k: v for k, v in obj.items() if v != ""}
    try:
        conn.sendall(json.dumps(response).encode())
    except:
        pass


def register(db: UserDatabase, conn, req):
    if not re.match("^\\w+$", req["user"]):
        res(conn, "Invalid username!")
        return

    if db.register(req["user"], req["passwd"]):
        res(conn, "Registered successfully. Please login!")
    else:
        res(conn, "Username already exists!")


def login(db: UserDatabase, conn, req):
    session_id = ""

    if db.login(req["user"], req["passwd"]):
        session_id = uuid4().hex
        SESSION[session_id] = {"user": req["user"], "conn": conn, "room_id": ""}
        res(conn, action="login", session_id=session_id)
    else:
        res(conn, "The username or password is incorrect!")

    return session_id


def logout(db: ChatroomDatabase, conn, req):
    out_room(db, conn, req)
    SESSION.pop(req["session_id"])


def new_room(db: ChatroomDatabase, conn, req):
    session_id = req["session_id"]
    if SESSION[session_id]["room_id"]:
        res(conn, "Please out current room first!")
        return
    res(conn, action="new_room", room_id=db.new_room())


def join_room(db: ChatroomDatabase, conn, req):
    session_id = req["session_id"]
    if SESSION[session_id]["room_id"]:
        res(conn, "Please out current room first!")
        return

    room_id = req["room_id"]
    msg = f'[*] {SESSION[session_id]["user"]} joined!'

    if db.join_room(room_id, session_id):
        SESSION[session_id]["room_id"] = room_id
        broadcast(db, room_id, session_id, msg)
        res(conn, "Joined!", "join_room", room_id=room_id)
    else:
        res(conn, "Invalid Room ID!")


def out_room(db: ChatroomDatabase, conn, req):
    session_id = req["session_id"]
    room_id = SESSION[session_id]["room_id"]

    if room_id:
        SESSION[session_id]["room_id"] = ""
        msg = f'[*] {SESSION[session_id]["user"]} is disconnected!'

        if db.remove_from_room(room_id, session_id):
            broadcast(db, room_id, session_id, msg)
        else:
            res(conn, "Failed to out room!")


def send_msg(db: ChatroomDatabase, req):
    session_id = req["session_id"]
    msg = f"{SESSION[session_id]['user']}: {req['msg']}"
    broadcast(db, SESSION[session_id]["room_id"], session_id, msg)


def disconnect_user(db: ChatroomDatabase, session_id):
    room_id = SESSION[session_id]["room_id"]
    if room_id:
        msg = f'[*] {SESSION[session_id]["user"]} is disconnected!'
        broadcast(db, room_id, session_id, msg)
