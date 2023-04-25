import sys
import threading

from login_register import LoginRegister
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from sock import Sock
from ui.main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    close_login_register_window = pyqtSignal()

    update_le_room_id = pyqtSignal(str, bool)
    update_lbl_username = pyqtSignal(str)
    append_txt_chat = pyqtSignal(str)

    show_popup = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        self.s = Sock()
        self.s_connected = False

    def connect_signals_slots(self):
        self.close_login_register_window.connect(
            self.handle_close_login_register_window_connected
        )
        self.update_lbl_username.connect(self.handle_update_lbl_username_connected)
        self.update_le_room_id.connect(self.handle_update_le_room_id_connected)
        self.append_txt_chat.connect(self.handle_append_txt_chat_connected)
        self.show_popup.connect(self.handle_show_popup_connected)

        self.le_input.returnPressed.connect(self.on_btn_send_clicked)

    # -- signal --
    def handle_close_login_register_window_connected(self):
        self.dial_login_register.accept()

    def handle_update_le_room_id_connected(self, room_id, read_only):
        self.le_room_id.setText(room_id)
        self.le_room_id.setReadOnly(read_only)

    def handle_update_lbl_username_connected(self, user):
        self.lbl_user.setText(user)

    def handle_append_txt_chat_connected(self, msg):
        self.txt_chat.append(msg)

    def handle_show_popup_connected(self, title, msg):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(msg)
        window.exec()

    # -- action --

    @pyqtSlot()
    def on_act_login_register_triggered(self):
        if not self.start_socket_daemon():
            return
        self.dial_login_register = LoginRegister(self.s, self)
        self.dial_login_register.exec()

    @pyqtSlot()
    def on_act_logout_triggered(self):
        if not self.check_logged_in():
            return

        self.send({"action": "logout"})
        self.s.session_id = ""
        self.txt_chat.clear()
        self.lbl_user.setText("Username")

        self.update_le_room_id.emit("", False)

    @pyqtSlot()
    def on_act_new_room_triggered(self):
        if not self.check_logged_in():
            return

        self.send({"action": "new_room"})

    @pyqtSlot()
    def on_act_out_room_triggered(self):
        if not self.check_logged_in() or not self.check_room_id():
            return
        self.send({"action": "out_room"})
        self.update_le_room_id.emit("", False)
        self.txt_chat.clear()

    @pyqtSlot()
    def on_act_quit_triggered(self):
        self.close()

    # -- button --

    @pyqtSlot()
    def on_btn_join_room_clicked(self):
        if not self.check_logged_in():
            return

        room_id = self.le_room_id.text()
        if room_id:
            self.send({"action": "join_room", "room_id": room_id})
        else:
            self.show_popup.emit("Error!", "Room ID is empty!")

    @pyqtSlot()
    def on_btn_send_clicked(self):
        if not self.check_logged_in() or not self.check_room_id():
            return
        msg = self.le_input.text()
        self.append_txt_chat.emit(f"{self.lbl_user.text()}: {msg}")
        self.send({"action": "send_msg", "msg": msg})

        self.le_input.clear()

    # -- other --

    def check_logged_in(self):
        if not self.s.session_id:
            self.show_popup.emit("Alert!", "Login first!")
            return False
        return True

    def check_room_id(self):
        if not self.le_room_id.text():
            self.show_popup.emit("Alert!", "Join or create a room first!")
            return False
        return True

    def send(self, obj):
        try:
            self.s.send(obj)
        except:
            self.s_connected = False
            self.show_popup.emit("Error!", "Server is disconnected!")

    # -- receive message thread --

    def listening_thread(self):
        while True:
            res = self.s.recv()
            if not res:
                break

            print(res)

            if "action" in res:
                action = res["action"]

                if action == "login":
                    self.s.session_id = res["session_id"]

                    user = self.dial_login_register.username
                    self.update_lbl_username.emit(user)
                    self.append_txt_chat.emit(f"[*] Welcome {user}!")

                    self.close_login_register_window.emit()

                elif action == "new_room":
                    self.update_le_room_id.emit(res["room_id"], True)
                    self.send({"action": "join_room", "room_id": res["room_id"]})
                elif action == "join_room":
                    self.update_le_room_id.emit(res["room_id"], True)
                elif action == "send_msg":
                    self.append_txt_chat.emit(res["msg"])
            else:
                self.show_popup.emit("Status", res["msg"])

    def start_socket_daemon(self):
        if not self.s_connected:
            try:
                self.s.connect()
                self.s_connected = True
                threading.Thread(target=self.listening_thread, daemon=True).start()
            except:
                self.show_popup.emit("Error!", "Please check your connection!")
                return False
        return True


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
