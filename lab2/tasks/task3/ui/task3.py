# Form implementation generated from reading ui file 'ui/task3.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dl_task3(object):
    def setupUi(self, dl_task3):
        dl_task3.setObjectName("dl_task3")
        dl_task3.resize(796, 420)
        dl_task3.setMinimumSize(QtCore.QSize(796, 420))
        self.verticalLayout = QtWidgets.QVBoxLayout(dl_task3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_read = QtWidgets.QPushButton(parent=dl_task3)
        self.btn_read.setObjectName("btn_read")
        self.horizontalLayout.addWidget(self.btn_read)
        self.btn_cal = QtWidgets.QPushButton(parent=dl_task3)
        self.btn_cal.setObjectName("btn_cal")
        self.horizontalLayout.addWidget(self.btn_cal)
        self.btn_write = QtWidgets.QPushButton(parent=dl_task3)
        self.btn_write.setObjectName("btn_write")
        self.horizontalLayout.addWidget(self.btn_write)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.te_input = QtWidgets.QTextEdit(parent=dl_task3)
        self.te_input.setObjectName("te_input")
        self.horizontalLayout_2.addWidget(self.te_input)
        self.te_output = QtWidgets.QTextEdit(parent=dl_task3)
        self.te_output.setObjectName("te_output")
        self.horizontalLayout_2.addWidget(self.te_output)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(dl_task3)
        QtCore.QMetaObject.connectSlotsByName(dl_task3)

    def retranslateUi(self, dl_task3):
        _translate = QtCore.QCoreApplication.translate
        dl_task3.setWindowTitle(_translate("dl_task3", "Read Expressions"))
        self.btn_read.setText(_translate("dl_task3", "Read"))
        self.btn_cal.setText(_translate("dl_task3", "Calculate"))
        self.btn_write.setText(_translate("dl_task3", "Write"))
