# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)
        Form.setMinimumSize(QtCore.QSize(500, 500))
        Form.setMaximumSize(QtCore.QSize(500, 500))
        Form.setWindowOpacity(1.0)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 481, 481))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.fa_table = QtWidgets.QTableView(self.verticalLayoutWidget)
        self.fa_table.setObjectName("fa_table")
        self.verticalLayout_3.addWidget(self.fa_table)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.regex_txt = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.regex_txt.setObjectName("regex_txt")
        self.horizontalLayout_2.addWidget(self.regex_txt)
        self.regex_to_fa_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.regex_to_fa_btn.setObjectName("regex_to_fa_btn")
        self.horizontalLayout_2.addWidget(self.regex_to_fa_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Formal Languages Simulator"))
        self.regex_txt.setPlaceholderText(_translate("Form", "Regex"))
        self.regex_to_fa_btn.setText(_translate("Form", "Regex > FA"))

