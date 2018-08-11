# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'banpick.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(442, 148)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.bpLayout = QtWidgets.QHBoxLayout()
        self.bpLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.bpLayout.setObjectName("bpLayout")
        self.mbpLayout = QtWidgets.QHBoxLayout()
        self.mbpLayout.setObjectName("mbpLayout")
        self.bpLayout.addLayout(self.mbpLayout)
        self.ebpLayout = QtWidgets.QHBoxLayout()
        self.ebpLayout.setObjectName("ebpLayout")
        self.bpLayout.addLayout(self.ebpLayout)
        self.verticalLayout.addLayout(self.bpLayout)
        self.resLayout = QtWidgets.QHBoxLayout()
        self.resLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.resLayout.setObjectName("resLayout")
        self.resEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.resEdit.setObjectName("resEdit")
        self.resLayout.addWidget(self.resEdit)
        self.verticalLayout.addLayout(self.resLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

