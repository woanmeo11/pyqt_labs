# Form implementation generated from reading ui file './tasks/task5/ui/task5.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dl_task5(object):
    def setupUi(self, dl_task5):
        dl_task5.setObjectName("dl_task5")
        dl_task5.resize(744, 472)
        dl_task5.setMinimumSize(QtCore.QSize(744, 472))
        self.verticalLayout = QtWidgets.QVBoxLayout(dl_task5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_path = QtWidgets.QLabel(parent=dl_task5)
        self.lbl_path.setObjectName("lbl_path")
        self.horizontalLayout.addWidget(self.lbl_path)
        self.le_path = QtWidgets.QLineEdit(parent=dl_task5)
        self.le_path.setObjectName("le_path")
        self.horizontalLayout.addWidget(self.le_path)
        self.btn_browse = QtWidgets.QPushButton(parent=dl_task5)
        self.btn_browse.setObjectName("btn_browse")
        self.horizontalLayout.addWidget(self.btn_browse)
        self.btn_back = QtWidgets.QPushButton(parent=dl_task5)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout.addWidget(self.btn_back)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tv_main = QtWidgets.QTreeView(parent=dl_task5)
        self.tv_main.setObjectName("tv_main")
        self.verticalLayout.addWidget(self.tv_main)

        self.retranslateUi(dl_task5)
        QtCore.QMetaObject.connectSlotsByName(dl_task5)

    def retranslateUi(self, dl_task5):
        _translate = QtCore.QCoreApplication.translate
        dl_task5.setWindowTitle(_translate("dl_task5", "File Explorer"))
        self.lbl_path.setText(_translate("dl_task5", "Path:"))
        self.btn_browse.setText(_translate("dl_task5", "Browse"))
        self.btn_back.setText(_translate("dl_task5", "Back"))
