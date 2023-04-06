from PyQt6.QtWidgets import QMessageBox


def alert(self, msg):
    window = QMessageBox()
    window.setText(msg)
    window.setWindowTitle("Error")
    window.exec()
