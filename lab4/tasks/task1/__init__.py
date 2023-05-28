import requests
from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from .ui.task1 import Ui_dl_task1


class Task1(QDialog, Ui_dl_task1):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_download.clicked.connect(self.handle_btn_download_clicked)

    def handle_btn_download_clicked(self):
        url = self.le_url.text()
        if not url:
            self.alert('Please enter URL!')
            return

        try:
            r = requests.get(self.le_url.text())
        except:
            self.alert('An error has occurred!')
            return

        self.te_source.setPlainText(r.text)

        self.tw_headers.setRowCount(0)
        for header, value in r.headers.items():
            pos = self.tw_headers.rowCount()
            self.tw_headers.insertRow(pos)
            self.tw_headers.setItem(pos, 0, QTableWidgetItem(header))
            self.tw_headers.setItem(pos, 1, QTableWidgetItem(value))

    def alert(self, msg):
        popup = QMessageBox(self)
        popup.setWindowTitle('Error')
        popup.setText(msg)
        popup.exec()
