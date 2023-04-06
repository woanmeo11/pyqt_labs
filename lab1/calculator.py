from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.calculator import Ui_calculator


class Calculator(QDialog, Ui_calculator):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_add.clicked.connect(lambda: self.handle_btn_operator_clicked("+"))
        self.btn_sub.clicked.connect(lambda: self.handle_btn_operator_clicked("-"))
        self.btn_mul.clicked.connect(lambda: self.handle_btn_operator_clicked("*"))
        self.btn_div.clicked.connect(lambda: self.handle_btn_operator_clicked("/"))

        self.btn_clear.clicked.connect(self.handle_btn_clear_clicked)
        self.btn_quit.clicked.connect(self.handle_btn_quit_clicked)

    def handle_btn_operator_clicked(self, operator):
        try:
            ans = float(self.le_num1.text())
            num = float(self.le_num2.text())

            if operator == "+":
                ans += num
            elif operator == "-":
                ans -= num
            elif operator == "*":
                ans *= num
            else:
                ans = round(ans / num, 2)

            if operator != "/":
                if ans.is_integer():
                    ans = int(ans)
                else:
                    raise ValueError()

            self.le_ans.setText(str(ans))

        except ValueError:
            self.alert("Please enter valid integer!")
        except ZeroDivisionError:
            self.alert("Second number cannot be zero!")

    def handle_btn_clear_clicked(self):
        self.le_num1.clear()
        self.le_num2.clear()
        self.le_ans.setText("0")

    def handle_btn_quit_clicked(self):
        self.close()

    def alert(self, msg):
        window = QMessageBox()
        window.setText(msg)
        window.setWindowTitle("Alert!")
        window.exec()

    def closeEvent(self, event):
        self.closed.emit()
