from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.base_converter import Ui_base_converter


class BaseConverter(QDialog, Ui_base_converter):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def closeEvent(self, event):
        self.closed.emit()

    def connect_signals_slots(self):
        self.btn_convert.clicked.connect(self.handle_btn_convert_clicked)

    def handle_btn_convert_clicked(self):
        if self.convert_from():
            self.convert_to()

    def convert_from(self):
        try:
            base = self.cb_frombase.currentText()

            if base == "Decimal":
                self.num = int(self.le_input.text())
            elif base == "Binary":
                self.num = int(self.le_input.text(), 2)
            else:
                self.num = int(self.le_input.text(), 16)
        except:
            self.alert("Please enter valid number!")
            self.le_ans.clear()
            return False

        return True

    def convert_to(self):
        base = self.cb_tobase.currentText()

        if base == "Decimal":
            ans = str(self.num)
        elif base == "Binary":
            ans = bin(self.num)[2:]
        else:
            ans = hex(self.num)[2:]

        self.le_ans.setText(ans)

    def alert(self, msg):
        window = QMessageBox()
        window.setText(msg)
        window.setWindowTitle("Alert!")
        window.exec()
