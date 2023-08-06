# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_vasp_supercell.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_UI_supercell(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(207, 185)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/结构.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("QPushButton{\n"
"color:rgb(255, 0, 0);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QLabel{\n"
"color:rgb(0, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QCheckBox{\n"
"color:rgb(0, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QGroupBox{\n"
"color:rgb(170, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QTextBrowser{\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QLineEdit{\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QTabWidget{\n"
"color:rgb(0, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"\n"
"QRadioButton{\n"
"color:rgb(0, 85, 255);\n"
"font: 12pt \"Times New Roman\";\n"
"}\n"
"")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_3.addWidget(self.lineEdit_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(90, 20))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Supercell"))
        self.groupBox.setTitle(_translate("Dialog", "Size of supercell"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:12pt;\">a:</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>b:</p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p>c:</p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Enter"))

