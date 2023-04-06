import csv

from PyQt6.QtWidgets import QDialog, QFileDialog, QTableWidgetItem
from utils.alert import alert

from .ui.student_info import Ui_dl_task4_student_info
from .ui.task4 import Ui_dl_task4


class StudentInfo(QDialog, Ui_dl_task4_student_info):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_add.clicked.connect(self.accept)

    @property
    def student_info(self):
        return [
            self.le_name.text(),
            self.le_id.text(),
            self.le_phone.text(),
            self.le_math.text(),
            self.le_lit.text(),
        ]


class Task4(QDialog, Ui_dl_task4):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        self.db = []

    def connect_signals_slots(self):
        self.btn_add.clicked.connect(self.handle_btn_add_clicked)
        self.btn_export.clicked.connect(self.handle_btn_export_clicked)
        self.btn_load.clicked.connect(self.handle_btn_load_clicked)

    def handle_btn_add_clicked(self):
        dialog = StudentInfo(self)
        if dialog.exec():
            self.db.append(dialog.student_info)
            self.add_items_to_table([dialog.student_info])
            self.write_csv("input.txt", self.db, ";")

    def handle_btn_export_clicked(self):
        self.db = []
        data = self.read_csv("input.txt", ";")
        for row in data:
            if row:
                row.append(self.get_gpa(row[-2], row[-1]))
                self.db.append(row)

        self.tb_info.setRowCount(0)
        self.add_items_to_table(self.db, True)

        if self.db:
            file_name, _ = QFileDialog.getSaveFileName(self, filter="Excel (*.csv)")
            if file_name:
                self.write_csv(file_name, self.db)

    def handle_btn_load_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, filter="Excel (*.csv)")
        if file_name:
            self.add_items_to_table(self.read_csv(file_name), True)

    def add_items_to_table(self, items, reset=False):
        if reset:
            self.tb_info.setRowCount(0)

        rcount = self.tb_info.rowCount()
        for i in range(len(items)):
            self.tb_info.insertRow(rcount + i)
            for j in range(len(items[i])):
                self.tb_info.setItem(rcount + i, j, QTableWidgetItem(items[i][j]))

    def get_gpa(self, a, b):
        try:
            gpa = (float(a) + float(b)) / 2
            if gpa.is_integer():
                return str(int(gpa))
            else:
                return str(round(gpa, 2))
        except:
            return "Error"

    def read_csv(self, file_name, delim=","):
        try:
            with open(file_name, "r", newline='') as f:
                csv_reader = csv.reader(f, delimiter=delim)
                return [row for row in csv_reader]
        except:
            alert(self, f"{file_name} not found!")
            return []

    def write_csv(self, file_name, contents, delim=","):
        with open(file_name, "w", newline='') as f:
            csv_writer = csv.writer(f, delimiter=delim)
            csv_writer.writerows(contents)
