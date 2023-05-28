import sys

from menu import Menu
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
menu = Menu()
menu.show()
sys.exit(app.exec())
