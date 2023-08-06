from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
                             QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
                             QTabWidget, QVBoxLayout, QWidget, QGridLayout)
from abinitostudio.structure.plot_structure import plot_str
import re, sys


class TabDialog(QDialog):
    def __init__(self, fileName, scene, parent=None):
        super(TabDialog, self).__init__(parent)
        self.fileName = fileName
        self.scene = scene
        fileInfo = QFileInfo(fileName)
        tabWidget = QTabWidget()
        self.abc = GeneralTab(fileInfo)
        tabWidget.addTab(self.abc, "General")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(self.plot_structure)
        self.buttonBox.rejected.connect(self.reject)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("Tab Dialog")

    def plot_structure(self):
        supertmp = self.abc.lineEdit1.text()
        self.supercell = self.tranform_to_integer(supertmp)
        print(self.supercell)
        plot_str(self.fileName, self.scene, self.supercell)

    def tranform_to_integer(self, text):
        super_tmp = re.split(r'[;,\s]', text)
        if len(super_tmp) != 3:
            print('please input three values for supercell!!')
            sys.exit()
        super_int = map(int, super_tmp)
        return tuple(super_int)


class GeneralTab(QWidget):
    def __init__(self, fileInfo, parent=None):
        super(GeneralTab, self).__init__(parent)
        fileNameLabel = QLabel("Size of supercell")
        label_a = QLabel("a: ")
        label_b = QLabel("b: ")
        label_c = QLabel("c: ")
        pathLabel = QLabel("Size of supercell")
        pathValueLabel = QLineEdit(fileInfo.fileName())
        sizeLabel = QLabel("Size:")
        size = fileInfo.size() // 1024
        sizeValueLabel = QLabel("%d K" % size)
        sizeValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        lastReadLabel = QLabel("Last Read:")
        lastReadValueLabel = QLabel(fileInfo.lastRead().toString())
        lastReadValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        lastModLabel = QLabel("Last Modified:")
        lastModValueLabel = QLabel(fileInfo.lastModified().toString())
        lastModValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        mainLayout = QGridLayout()
        mainLayout.addWidget(fileNameLabel, 0, 1)
        mainLayout.addWidget(label_a, 1, 0)
        mainLayout.addWidget(label_b, 2, 0)
        mainLayout.addWidget(label_c, 3, 0)
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
        mainLayout.addWidget(self.lineEdit1, 1, 1)
        mainLayout.addWidget(self.lineEdit2, 2, 1)
        mainLayout.addWidget(self.lineEdit3, 3, 1)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "."
    tabdialog = TabDialog(fileName)
    tabdialog.show()
    sys.exit(app.exec_())
