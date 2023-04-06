from base_converter import BaseConverter
from calculator import Calculator
from grade_management import GradeManagement
from min_max import Min_Max
from number_to_vntext import NumberToVNText
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from ui.menu import Ui_menu


class Menu(QMainWindow, Ui_menu):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.btn_task1.clicked.connect(lambda: self.openChild(Calculator))
        self.btn_task2.clicked.connect(lambda: self.openChild(Min_Max))
        self.btn_task3.clicked.connect(lambda: self.openChild(NumberToVNText))
        self.btn_task4.clicked.connect(lambda: self.openChild(BaseConverter))
        self.btn_task5.clicked.connect(lambda: self.openChild(GradeManagement))

    def openChild(self, childClass):
        self.hide()
        self.child = childClass(self)
        self.child.show()
        self.child.closed.connect(self.show)

    def closeEvent(self, event):
        self.closed.emit()
