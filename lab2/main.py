import sys

sys.dont_write_bytecode = True

from menu import Menu
from PyQt6.QtWidgets import QApplication

app = QApplication([])
menu = Menu()
menu.show()
sys.exit(app.exec())
