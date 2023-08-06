# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(553, 448)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/结构.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QPushButton{\ncolor:rgb(255, 0, 0);\nfont: 12pt \"宋体\";\n}\n\n"
                                 "QLabel{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"宋体\";\n}\n\n"
                                 "QCheckBox{\ncolor:rgb(0, 85, 255);\nfont: 12pt \"宋体\";\n}\n\n"
                                 "QGroupBox{\ncolor:rgb(170, 85, 255);\nfont: 12pt \"宋体\";\n}\n\n"
                                 "QTextBrowser{\nfont: 12pt \"宋体\";\n}\n\n"
                                 "QLineEdit{\nfont: 12pt \"宋体\";\n}\n\n")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.textBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.textBrowser.setObjectName("textBrowser")

        self.horizontalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 553, 23))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.menuVASP = QtWidgets.QMenu(self.menu)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/vasp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuVASP.setIcon(icon1)
        self.menuVASP.setObjectName("menuVASP")

        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")

        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")

        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.actionclose = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/关闭.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionclose.setIcon(icon2)
        self.actionclose.setObjectName("actionclose")

        self.actionband = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/能带.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionband.setIcon(icon3)
        self.actionband.setObjectName("actionband")

        self.actionprojectionband = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/态密度.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionprojectionband.setIcon(icon4)
        self.actionprojectionband.setObjectName("actionprojectionband")

        self.actiondos = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/投影能带.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondos.setIcon(icon5)
        self.actiondos.setObjectName("actiondos")

        self.actionchgcar = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/投影能带.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionchgcar.setIcon(icon5)
        self.actionchgcar.setObjectName("actionCHGCAR")

        self.actioninstruction = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/说明.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioninstruction.setIcon(icon6)
        self.actioninstruction.setObjectName("actioninstruction")

        self.actionabout = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/关于.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionabout.setIcon(icon7)
        self.actionabout.setObjectName("actionabout")

        self.actionsupercell = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/扩胞.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsupercell.setIcon(icon8)
        self.actionsupercell.setObjectName("actionsupercell")

        self.actionsetting = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("images/设置.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsetting.setIcon(icon9)
        self.actionsetting.setObjectName("actionsetting")

        self.actiontest = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("images/测试.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiontest.setIcon(icon10)
        self.actiontest.setObjectName("actiontest")

        self.actionvisual = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("images/3d可视.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionvisual.setIcon(icon11)
        self.actionvisual.setObjectName("actionvisual")

        self.actionbands = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("images/band.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionbands.setIcon(icon12)
        self.actionbands.setObjectName("actionbands")

        self.actionscf = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("images/scf.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionscf.setIcon(icon13)
        self.actionscf.setObjectName("actionscf")

        self.actionscf_noncal = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("images/scf_noncal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionscf_noncal.setIcon(icon14)
        self.actionscf_noncal.setObjectName("actionscf_noncal")

        self.actionband_noncal = QtWidgets.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("images/band_noncal.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionband_noncal.setIcon(icon15)
        self.actionband_noncal.setObjectName("actionband_noncal")

        self.actionDOS = QtWidgets.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap("images/DOS.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDOS.setIcon(icon16)
        self.actionDOS.setObjectName("actionDOS")

        self.actionphonon = QtWidgets.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap("images/phonin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionphonon.setIcon(icon17)
        self.actionphonon.setObjectName("actionphonon")

        self.actionwannier = QtWidgets.QAction(MainWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap("images/wannier.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionwannier.setIcon(icon18)
        self.actionwannier.setObjectName("actionwannier")

        self.menuFile.addAction(self.actionvisual)
        self.menuFile.addAction(self.actionclose)

        self.menuOperation.addAction(self.actionband)
        self.menuOperation.addAction(self.actionprojectionband)
        self.menuOperation.addAction(self.actiondos)
        self.menuOperation.addAction(self.actionchgcar)

        self.menuHelp.addAction(self.actioninstruction)
        self.menuHelp.addAction(self.actionabout)

        self.menuVASP.addAction(self.actionscf)
        self.menuVASP.addAction(self.actionscf_noncal)
        self.menuVASP.addAction(self.actionbands)
        self.menuVASP.addAction(self.actionband_noncal)
        self.menuVASP.addAction(self.actionDOS)
        self.menuVASP.addAction(self.actionphonon)
        self.menuVASP.addAction(self.actionwannier)

        self.menu.addAction(self.actiontest)
        self.menu.addAction(self.menuVASP.menuAction())

        self.menu_2.addAction(self.actionsetting)
        self.menu_4.addAction(self.actionsupercell)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuOperation.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionclose)
        self.toolBar.addAction(self.actionsupercell)

        self.retranslateUi(MainWindow)
        self.actionclose.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Abinito Studio 1.0"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionvisual.setText(_translate("MainWindow", "Open POSCAR"))
        self.actionvisual.setToolTip(_translate("MainWindow", "打开POSCAR"))
        self.actionclose.setText(_translate("MainWindow", "Close"))

        self.menu.setTitle(_translate("MainWindow", "Calculation"))
        self.actiontest.setText(_translate("MainWindow", "Pyxtal"))
        self.actiontest.setToolTip(_translate("MainWindow", "test"))
        self.menuVASP.setTitle(_translate("MainWindow", "VASP"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionscf.setText(_translate("MainWindow", "scf"))
        self.actionscf_noncal.setText(_translate("MainWindow", "scf_noncal"))
        self.actionbands.setText(_translate("MainWindow", "band"))
        self.actionband_noncal.setText(_translate("MainWindow", "band_noncal"))
        self.actionDOS.setText(_translate("MainWindow", "DOS"))
        self.actionphonon.setText(_translate("MainWindow", "phonon"))
        self.actionwannier.setText(_translate("MainWindow", "wannier"))

        self.menuOperation.setTitle(_translate("MainWindow", "Plot"))
        self.actionband.setText(_translate("MainWindow", "Bands"))
        self.actionband.setToolTip(_translate("MainWindow", "Plot bands"))
        self.actionprojectionband.setText(_translate("MainWindow", "Projected Band"))
        self.actionprojectionband.setToolTip(_translate("MainWindow", "Plot projected bands"))
        self.actiondos.setText(_translate("MainWindow", "DOS"))
        self.actiondos.setToolTip(_translate("MainWindow", "Plot DOS"))
        self.actionchgcar.setText(_translate("MainWindow", "CHGCAR"))
        self.actionchgcar.setToolTip(_translate("MainWindow", "Plot CHGCAR of VASP"))

        self.menu_4.setTitle(_translate("MainWindow", "Tools"))
        self.actionsupercell.setText(_translate("MainWindow", "Supercell"))
        self.actionsupercell.setToolTip(_translate("MainWindow", "Build supercell"))

        self.menu_2.setTitle(_translate("MainWindow", "Settings"))
        self.actionsetting.setText(_translate("MainWindow", "Node Connection"))
        self.actionsetting.setToolTip(_translate("MainWindow", "节点设置"))

        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actioninstruction.setText(_translate("MainWindow", "Instruction"))
        self.actioninstruction.setToolTip(_translate("MainWindow", "说明"))
        self.actionabout.setText(_translate("MainWindow", "About"))
        self.actionabout.setToolTip(_translate("MainWindow", "关于"))
