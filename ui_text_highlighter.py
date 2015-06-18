# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'texthighlighter.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TextHighlighter(object):
    def setupUi(self, TextHighlighter):
        TextHighlighter.setObjectName("TextHighlighter")
        TextHighlighter.resize(400, 400)
        TextHighlighter.setMinimumSize(QtCore.QSize(400, 400))
        TextHighlighter.setMaximumSize(QtCore.QSize(400, 400))
        self.plainTextEdit = QtWidgets.QPlainTextEdit(TextHighlighter)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 381, 381))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(TextHighlighter)
        QtCore.QMetaObject.connectSlotsByName(TextHighlighter)

    def retranslateUi(self, TextHighlighter):
        _translate = QtCore.QCoreApplication.translate
        TextHighlighter.setWindowTitle(_translate("TextHighlighter", "Procurar no texto"))
        self.plainTextEdit.setProperty("placeholderText", _translate("TextHighlighter", "Entre com o texto aqui"))

