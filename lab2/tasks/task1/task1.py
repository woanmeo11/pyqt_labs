from PyQt6.QtWidgets import QDialog, QFileDialog

from .ui.task1 import Ui_dl_task1


class Task1(QDialog, Ui_dl_task1):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_to_upper.clicked.connect(self.handle_btn_to_upper_clicked)
        self.btn_to_lower.clicked.connect(self.handle_btn_to_lower_clicked)
        self.btn_read.clicked.connect(self.handle_btn_read_clicked)
        self.btn_write.clicked.connect(self.handle_btn_write_clicked)

    def handle_btn_to_upper_clicked(self):
        self.te_content.setText(self.te_content.toPlainText().upper())

    def handle_btn_to_lower_clicked(self):
        self.te_content.setText(self.te_content.toPlainText().lower())

    def handle_btn_read_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, filter="Text Files (*.txt)")
        if file_name:
            with open(file_name, "r") as f:
                self.te_content.setText(f.read())

    def handle_btn_write_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, filter="Text Files (*.txt)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.te_content.toPlainText())
