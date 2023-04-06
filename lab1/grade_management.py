from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QLabel, QMessageBox
from ui.grade_management import Ui_grade_management


class GradeManagement(QDialog, Ui_grade_management):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def closeEvent(self, event):
        self.closed.emit()

    def connect_signals_slots(self):
        self.btn_calculate.clicked.connect(self.handle_btn_calculate_clicked)

    def handle_btn_calculate_clicked(self):
        if not self.parse_grade_list():
            return

        self.clear_gb()
        self.write_to_gb()
        self.calculate_properties()

    def parse_number(self, text):
        num = float(text)
        return int(num) if num.is_integer() else num

    def parse_grade_list(self):
        try:
            arr = self.le_grade_list.text().split()
            self.gl = list(map(self.parse_number, arr))
        except:
            self.alert("Please enter valid grade list!")
            return False

        return True

    def clear_gb(self):
        for i in reversed(range(self.gb_gridlayout_main.count())):
            self.gb_gridlayout_main.itemAt(i).widget().deleteLater()

    def write_to_gb(self):
        for i in range(len(self.gl)):
            new_lbl = QLabel(self.gb_list_subjects_grades)
            new_lbl.setText(f"Course {i + 1}: {self.gl[i]}")
            self.gb_gridlayout_main.addWidget(new_lbl, i // 10, i % 10, 1, 1)

    def calculate_properties(self):
        self.lbl_gpa.setText(str(round(sum(self.gl) / len(self.gl), 2)))
        self.lbl_hg.setText(str(max(self.gl)))
        self.lbl_lg.setText(str(min(self.gl)))
        self.lbl_ncp.setText(str(sum(i >= 5 for i in self.gl)))
        self.lbl_ncnp.setText(str(len(self.gl) - int(self.lbl_ncp.text())))
        self.lbl_apc.setText(self.get_performance_classify())

    def get_performance_classify(self):
        gpa = float(self.lbl_gpa.text())

        if gpa >= 8 and all(i >= 6.5 for i in self.gl):
            return "Excellent"
        elif gpa >= 6.5 and all(i >= 5 for i in self.gl):
            return "Good"
        elif gpa >= 5 and all(i >= 3.5 for i in self.gl):
            return "Average"
        elif gpa >= 3.5 and all(i >= 2 for i in self.gl):
            return "Below Average"
        else:
            return "Poor"

    def alert(self, msg):
        window = QMessageBox()
        window.setText(msg)
        window.setWindowTitle("Alert!")
        window.exec()
