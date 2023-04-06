from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.min_max import Ui_min_max


class Min_Max(QDialog, Ui_min_max):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def closeEvent(self, event):
        self.closed.emit()

    def connect_signals_slots(self):
        self.btn_find.clicked.connect(self.handle_btn_find_clicked)
        self.btn_clear.clicked.connect(self.handle_btn_clear_clicked)
        self.btn_quit.clicked.connect(self.handle_btn_quit_clicked)

    def parse_number(self, line_edit):
        num = float(line_edit.text())
        return int(num) if num.is_integer() else num

    def transfrom(self, func, arr):
        return str(func(list(map(self.parse_number, arr))))

    def handle_btn_find_clicked(self):
        le_inputs = [self.le_num1, self.le_num2, self.le_num3]

        try:
            self.le_min.setText(self.transfrom(min, le_inputs))
            self.le_max.setText(self.transfrom(max, le_inputs))
        except:
            self.alert("Please enter valid number!")
            return

    def handle_btn_clear_clicked(self):
        self.le_num1.clear()
        self.le_num2.clear()
        self.le_num3.clear()
        self.le_min.clear()
        self.le_max.clear()

    def handle_btn_quit_clicked(self):
        self.close()

    def alert(self, msg):
        window = QMessageBox()
        window.setText(msg)
        window.setWindowTitle("Alert!")
        window.exec()
