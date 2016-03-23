# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'popUp.ui'
#
# Created: Wed Mar 23 00:14:23 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.Qt import *
import pickle
import os.path
import numpy as np
from fileinput import filename
from pip._vendor.ipaddress import summarize_address_range

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(485, 595)
        Dialog.setInputMethodHints(QtCore.Qt.ImhNone)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit_groupName = QtGui.QLineEdit(Dialog)
        self.lineEdit_groupName.setObjectName(_fromUtf8("lineEdit_groupName"))
        self.gridLayout.addWidget(self.lineEdit_groupName, 1, 1, 1, 1)
        self.lbl_designer = QtGui.QLabel(Dialog)
        self.lbl_designer.setObjectName(_fromUtf8("lbl_designer"))
        self.gridLayout.addWidget(self.lbl_designer, 1, 0, 1, 1)
        self.lbl_companyName = QtGui.QLabel(Dialog)
        self.lbl_companyName.setObjectName(_fromUtf8("lbl_companyName"))
        self.gridLayout.addWidget(self.lbl_companyName, 0, 0, 1, 1)
        self.lineEdit_designer = QtGui.QLineEdit(Dialog)
        self.lineEdit_designer.setObjectName(_fromUtf8("lineEdit_designer"))
        self.gridLayout.addWidget(self.lineEdit_designer, 2, 1, 1, 1)
        self.lineEdit_companyName = QtGui.QLineEdit(Dialog)
        self.lineEdit_companyName.setObjectName(_fromUtf8("lineEdit_companyName"))
        self.gridLayout.addWidget(self.lineEdit_companyName, 0, 1, 1, 1)
        self.lbl_groupName = QtGui.QLabel(Dialog)
        self.lbl_groupName.setObjectName(_fromUtf8("lbl_groupName"))
        self.gridLayout.addWidget(self.lbl_groupName, 2, 0, 1, 1)
        self.lineEdit_projectTitle = QtGui.QLineEdit(Dialog)
        self.lineEdit_projectTitle.setObjectName(_fromUtf8("lineEdit_projectTitle"))
        self.gridLayout.addWidget(self.lineEdit_projectTitle, 4, 1, 1, 1)
        self.lineEdit_jobNumber = QtGui.QLineEdit(Dialog)
        self.lineEdit_jobNumber.setObjectName(_fromUtf8("lineEdit_jobNumber"))
        self.gridLayout.addWidget(self.lineEdit_jobNumber, 3, 1, 1, 1)
        self.lbl_jobNumber = QtGui.QLabel(Dialog)
        self.lbl_jobNumber.setObjectName(_fromUtf8("lbl_jobNumber"))
        self.gridLayout.addWidget(self.lbl_jobNumber, 4, 0, 1, 1)
        self.lbl_projectTitle = QtGui.QLabel(Dialog)
        self.lbl_projectTitle.setObjectName(_fromUtf8("lbl_projectTitle"))
        self.gridLayout.addWidget(self.lbl_projectTitle, 3, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 7, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.lbl_designer.setText(_translate("Dialog", "Designer :", None))
        self.lbl_companyName.setText(_translate("Dialog", "Company Name :", None))
        self.lbl_groupName.setText(_translate("Dialog", "Group/Team Name :", None))
        self.lbl_jobNumber.setText(_translate("Dialog", "Job Number :", None))
        self.lbl_projectTitle.setText(_translate("Dialog", "Project Title :", None))
        self.pushButton.setText(_translate("Dialog", "ok", None))

