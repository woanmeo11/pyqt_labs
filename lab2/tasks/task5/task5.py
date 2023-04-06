import os

from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QDialog, QFileDialog

from .ui.task5 import Ui_dl_task5


class Task5(QDialog, Ui_dl_task5):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_file_system_tree_view()
        self.connect_signals_slots()

    def init_file_system_tree_view(self):
        self.current_path = QDir.currentPath()
        self.model = QFileSystemModel()
        self.model.setRootPath(self.current_path)

        self.tv_main.setModel(self.model)
        self.tv_main.setItemsExpandable(False)
        self.tv_main.setRootIsDecorated(False)

        self.update_tree_view(self.current_path)

    def connect_signals_slots(self):
        self.btn_browse.clicked.connect(self.handle_btn_browse_clicked)
        self.btn_back.clicked.connect(self.handle_btn_back_clicked)
        self.tv_main.doubleClicked.connect(self.handle_tv_main_doubleClicked)

    def handle_btn_browse_clicked(self):
        path = QFileDialog.getExistingDirectory(
            self, options=QFileDialog.Option.ShowDirsOnly
        )
        if path:
            self.update_tree_view(path)

    def handle_btn_back_clicked(self):
        self.update_tree_view(os.path.dirname(self.current_path))

    def handle_tv_main_doubleClicked(self, index):
        self.update_tree_view(index.model().filePath(index))

    def update_tree_view(self, path):
        self.current_path = path
        self.tv_main.setRootIndex(self.model.index(self.current_path))
        self.le_path.setText(self.current_path)
