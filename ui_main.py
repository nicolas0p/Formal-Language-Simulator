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
        Form.resize(850, 500)
        Form.setMinimumSize(QtCore.QSize(850, 500))
        Form.setMaximumSize(QtCore.QSize(850, 500))
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 851, 501))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.er_equals_gr_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.er_equals_gr_btn.setObjectName("er_equals_gr_btn")
        self.gridLayout.addWidget(self.er_equals_gr_btn, 2, 1, 1, 1)
        self.int_fa_a_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.int_fa_a_btn.setObjectName("int_fa_a_btn")
        self.gridLayout.addWidget(self.int_fa_a_btn, 2, 2, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 261, 201))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gr_text = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget_2)
        self.gr_text.setObjectName("gr_text")
        self.verticalLayout_2.addWidget(self.gr_text)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gr_fa_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.gr_fa_a_btn.setObjectName("gr_fa_a_btn")
        self.gridLayout_3.addWidget(self.gr_fa_a_btn, 0, 0, 1, 1)
        self.gr_fa_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.gr_fa_b_btn.setObjectName("gr_fa_b_btn")
        self.gridLayout_3.addWidget(self.gr_fa_b_btn, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout.addWidget(self.groupBox_3, 3, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 341, 201))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.fa_a_table = QtWidgets.QTableWidget(self.verticalLayoutWidget_3)
        self.fa_a_table.setObjectName("fa_a_table")
        self.fa_a_table.setColumnCount(0)
        self.fa_a_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.fa_a_table)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.min_fa_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.min_fa_a_btn.setObjectName("min_fa_a_btn")
        self.gridLayout_4.addWidget(self.min_fa_a_btn, 0, 1, 1, 1)
        self.det_af_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.det_af_a_btn.setObjectName("det_af_a_btn")
        self.gridLayout_4.addWidget(self.det_af_a_btn, 0, 0, 1, 1)
        self.com_fa_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.com_fa_a_btn.setObjectName("com_fa_a_btn")
        self.gridLayout_4.addWidget(self.com_fa_a_btn, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_4)
        self.gridLayout.addWidget(self.groupBox_2, 1, 2, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_4)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 20, 341, 201))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.fa_b_table = QtWidgets.QTableView(self.verticalLayoutWidget_4)
        self.fa_b_table.setObjectName("fa_b_table")
        self.verticalLayout_4.addWidget(self.fa_b_table)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.min_fa_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.min_fa_b_btn.setObjectName("min_fa_b_btn")
        self.gridLayout_5.addWidget(self.min_fa_b_btn, 0, 1, 1, 1)
        self.det_fa_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.det_fa_b_btn.setObjectName("det_fa_b_btn")
        self.gridLayout_5.addWidget(self.det_fa_b_btn, 0, 0, 1, 1)
        self.com_fa_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.com_fa_b_btn.setObjectName("com_fa_b_btn")
        self.gridLayout_5.addWidget(self.com_fa_b_btn, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_5)
        self.gridLayout.addWidget(self.groupBox_4, 3, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 261, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.er_text = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.er_text.setObjectName("er_text")
        self.verticalLayout.addWidget(self.er_text)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.er_fa_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.er_fa_b_btn.setObjectName("er_fa_b_btn")
        self.gridLayout_2.addWidget(self.er_fa_b_btn, 0, 1, 1, 1)
        self.er_fa_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.er_fa_a_btn.setObjectName("er_fa_a_btn")
        self.gridLayout_2.addWidget(self.er_fa_a_btn, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.er_search_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.er_search_btn.setObjectName("er_search_btn")
        self.verticalLayout.addWidget(self.er_search_btn)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(1, 62)
        self.gridLayout.setColumnStretch(2, 80)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.groupBox_5)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(-1, 20, 191, 461))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.fa_list = QtWidgets.QListView(self.verticalLayoutWidget_6)
        self.fa_list.setObjectName("fa_list")
        self.verticalLayout_6.addWidget(self.fa_list)
        self.fa_list_a_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.fa_list_a_btn.setObjectName("fa_list_a_btn")
        self.verticalLayout_6.addWidget(self.fa_list_a_btn)
        self.fa_list_b_btn = QtWidgets.QPushButton(self.verticalLayoutWidget_6)
        self.fa_list_b_btn.setObjectName("fa_list_b_btn")
        self.verticalLayout_6.addWidget(self.fa_list_b_btn)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.horizontalLayout.setStretch(0, 40)
        self.horizontalLayout.setStretch(1, 12)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Formal Language Simulator - Nícolas Pfeifer & Evandro Sasse"))
        self.er_equals_gr_btn.setText(_translate("Form", "Verificar Equivalência entre ER e GR"))
        self.int_fa_a_btn.setText(_translate("Form", "Intersecção entre os AFs - Slot A"))
        self.groupBox_3.setTitle(_translate("Form", "Gramática Regular"))
        self.gr_text.setPlaceholderText(_translate("Form", "S -> aS | b "))
        self.gr_fa_a_btn.setText(_translate("Form", "GR p/ AF - Slot A"))
        self.gr_fa_b_btn.setText(_translate("Form", "GR p/ AF - Slot B"))
        self.groupBox_2.setTitle(_translate("Form", "Autômato Finito - Slot A"))
        self.min_fa_a_btn.setText(_translate("Form", "Minimizar"))
        self.det_af_a_btn.setText(_translate("Form", "Determinizar"))
        self.com_fa_a_btn.setText(_translate("Form", "Complemento"))
        self.groupBox_4.setTitle(_translate("Form", "Autômato Finito - Slot B"))
        self.min_fa_b_btn.setText(_translate("Form", "Minimizar"))
        self.det_fa_b_btn.setText(_translate("Form", "Determinizar"))
        self.com_fa_b_btn.setText(_translate("Form", "Complemento"))
        self.groupBox.setTitle(_translate("Form", "Expressão Regular"))
        self.er_text.setPlaceholderText(_translate("Form", "(0*(1(01*0)*1)*0*)*"))
        self.er_fa_b_btn.setText(_translate("Form", "ER p/ AF - Slot B"))
        self.er_fa_a_btn.setText(_translate("Form", "ER p/ AF - Slot A"))
        self.er_search_btn.setText(_translate("Form", "Procurar em texto usando esta ER"))
        self.groupBox_5.setTitle(_translate("Form", "Autômatos das operações"))
        self.fa_list_a_btn.setText(_translate("Form", "Enviar para o Slot A"))
        self.fa_list_b_btn.setText(_translate("Form", "Enviar para o Slot B"))

