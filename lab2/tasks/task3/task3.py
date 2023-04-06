import re

from PyQt6.QtWidgets import QDialog, QFileDialog
from utils.alert import alert

from .ui.task3 import Ui_dl_task3


class Task3(QDialog, Ui_dl_task3):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_read.clicked.connect(self.handle_btn_read_clicked)
        self.btn_write.clicked.connect(self.handle_btn_write_clicked)
        self.btn_cal.clicked.connect(self.handle_btn_cal_clicked)

    def handle_btn_read_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self)
        if not file_name:
            return

        try:
            with open(file_name, "r") as f:
                self.te_input.setText(f.read())
        except UnicodeDecodeError:
            alert(self, "File contains invalid character!")

    def handle_btn_write_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self)
        if not file_name:
            return

        try:
            with open(file_name, "w") as f:
                f.write(self.te_output.toPlainText())
        except UnicodeDecodeError:
            alert(self, "File contains invalid character!")

    def handle_btn_cal_clicked(self):
        contents = ""
        for line in self.te_input.toPlainText().splitlines():
            line = line.strip()
            try:
                if self.check_valid_expression(line):
                    ans = str(eval(line))
                else:
                    raise Exception
            except:
                ans = "Invalid expression!"
            contents += f"{line} = {ans}\n"
        self.te_output.setText(contents)

    def check_valid_expression(self, expr):
        return re.match("^[\\d+\\-*\\/%\\s]+$", expr)
