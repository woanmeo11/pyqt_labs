from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.number_to_vntext import Ui_number_to_vntext
from utils.vn_number_converter import VNNumConverter


class NumberToVNText(QDialog, Ui_number_to_vntext):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        self.converter = VNNumConverter()

    def connect_signals_slots(self):
        self.btn_convert.clicked.connect(self.handle_btn_convert_clicked)
        self.btn_clear.clicked.connect(self.handle_btn_clear_clicked)
        self.btn_quit.clicked.connect(self.handle_btn_quit_clicked)

    def handle_btn_convert_clicked(self):
        try:
            num = int(self.le_input.text())
            self.le_ans.setText(" ".join(self.converter.number_to_vntext(num)).strip())
        except:
            self.alert("Please enter valid number!")

    def handle_btn_clear_clicked(self):
        self.le_input.clear()
        self.le_ans.clear()

    def handle_btn_quit_clicked(self):
        self.close()

    def closeEvent(self, event):
        self.closed.emit()

    def alert(self, msg):
        window = QMessageBox()
        window.setText(msg)
        window.setWindowTitle("Alert!")
        window.exec()
