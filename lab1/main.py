import sys

from menu import Menu
from PyQt6.QtWidgets import QApplication

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

menu = Menu()
menu.show()
menu.closed.connect(app.quit)

sys.exit(app.exec())
