from os import path

from PyQt6.QtWidgets import QDialog, QFileDialog

from .ui.task2 import Ui_dl_task2


class Task2(QDialog, Ui_dl_task2):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_read_file.clicked.connect(self.read_file)

    def read_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, filter="Text Files (*.txt)")
        if file_name:
            with open(file_name, "r") as f:
                self.te_content.setText(f.read())

            contents = self.te_content.toPlainText()

            self.le_name.setText(path.basename(file_name))
            self.le_url.setText(file_name)

            self.le_word.setText(str(len(contents.split())))
            self.le_char.setText(str(len(contents)))

            if len(contents) and contents[-1] != "\n":
                n = 1
            else:
                n = 0
            self.le_line.setText(str(contents.count("\n") + n))
