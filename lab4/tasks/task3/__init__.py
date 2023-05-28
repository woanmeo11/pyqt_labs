import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDialog, QMessageBox

from .ui.task3 import Ui_dl_task3


class Task3(QDialog, Ui_dl_task3):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_get.clicked.connect(self.handle_btn_get_clicked)

    def handle_btn_get_clicked(self):
        try:
            r = requests.get("http://127.0.0.1:8000/api/random_catto")
            file_name = r.json()['file_name']
            image_bytes = requests.get("http://127.0.0.1:8000/api/get/" + file_name).content
        except:
            popup = QMessageBox(self)
            popup.setWindowTitle("Error!")
            popup.setText("Please run the server!")
            popup.exec()
            return

        self.lbl_file_name.setText(file_name)
        pm = QPixmap.fromImage(QImage.fromData(image_bytes))
        self.lbl_image.setPixmap(
            pm.scaled(self.lbl_image.width(), self.lbl_image.height(),
                      Qt.AspectRatioMode.KeepAspectRatio))
