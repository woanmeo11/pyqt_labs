from PyQt6.QtWidgets import QDialog, QLineEdit, QMessageBox
from ui.login_register import Ui_dl_login_register


class LoginRegister(QDialog, Ui_dl_login_register):
    def __init__(self, sock, parent=None):
        self.s = sock
        self.__user = ""

        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)

    def connect_signals_slots(self):
        self.btn_login.clicked.connect(self.handle_btn_login_register_clicked)
        self.btn_register.clicked.connect(
            lambda: self.handle_btn_login_register_clicked(True)
        )

    @property
    def username(self):
        return self.__user

    def handle_btn_login_register_clicked(self, register=False):
        if self.s.session_id:
            self.popup("Error!", "Logout first!")
            return

        user = self.le_username.text()
        passwd = self.le_password.text()

        if not user:
            self.popup("Error!", "Username can not be empty!")
        elif not passwd:
            self.popup("Error!", "Password can not be empty!")
        elif register:
            self.s.send({"action": "register", "user": user, "passwd": passwd})
        else:
            self.__user = user
            self.s.send({"action": "login", "user": user, "passwd": passwd})

    def on_btn_close_clicked(self):
        self.close()

    def popup(self, title, msg):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(msg)
        window.exec()
