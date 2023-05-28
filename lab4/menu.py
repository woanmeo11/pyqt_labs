from PyQt6.QtWidgets import QMainWindow
from tasks.task1 import Task1
from tasks.task2 import Task2
from tasks.task3 import Task3
from tasks.task4 import Task4
from ui.menu import Ui_menu


class Menu(QMainWindow, Ui_menu):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_task1.clicked.connect(lambda: self.openChild(Task1))
        self.btn_task2.clicked.connect(lambda: self.openChild(Task2))
        self.btn_task3.clicked.connect(lambda: self.openChild(Task3))
        self.btn_task4.clicked.connect(lambda: self.openChild(Task4))

    def openChild(self, childClass):
        self.hide()
        childClass(self).exec()
        self.show()
