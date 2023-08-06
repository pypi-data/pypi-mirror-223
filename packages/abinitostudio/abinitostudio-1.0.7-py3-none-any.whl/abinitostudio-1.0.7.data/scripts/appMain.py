##  GUI应用程序主程序入口

import sys

from PyQt5.QtWidgets import QApplication,QSplashScreen
from PyQt5 import QtGui,QtCore,QtWidgets

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)

app = QApplication(sys.argv)  # 创建GUI应用程序

splash = QSplashScreen(QtGui.QPixmap("abinitostudio\images\startup.jpg"))
splash.showMessage("The program is loading, please wait...", \
                   QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
splash.show()                       # 显示启动界面
QtWidgets.qApp.processEvents()        # 处理主进程事件

from abinitostudio.myMainWindow import MainWindow
mainform = MainWindow()  # 创建主窗体
mainform.showMaximized()  # 最大化窗口
mainform.show()  # 显示主窗体

splash.finish(mainform)                 # 隐藏启动界面

sys.exit(app.exec_())
