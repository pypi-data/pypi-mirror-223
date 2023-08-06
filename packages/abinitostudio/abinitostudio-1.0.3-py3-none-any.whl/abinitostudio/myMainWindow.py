import sys, os, paramiko, ase.io.vasp
import numpy as np
from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QAction, \
    QColorDialog, QFileDialog
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QDragEnterEvent, QPixmap
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
import matplotlib.pyplot as plt
from mayavi.core.ui.api import (MayaviScene, MlabSceneModel, SceneEditor)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
sys.path.append('..')
from abinitostudio.structure.plot_structure import plot_str
from abinitostudio.structure.tabdialog import *
from functools import partial
from pyxtal import pyxtal
from jumpssh import SSHSession
from abinitostudio.ui import UI
from abinitostudio.ui.UI_test import Ui_Form_UI_test
from abinitostudio.ui.UI_setting import Ui_Form_UI_setting
from abinitostudio.ui.UI_vasp_scf import Ui_Form_UI_vasp_scf
from abinitostudio.ui.UI_vasp_scf_noncal import Ui_Form_UI_vasp_scf_noncal
from abinitostudio.ui.UI_vasp_band import Ui_Form_UI_vasp_band
from abinitostudio.ui.UI_vasp_band_noncal import Ui_Form_UI_vasp_band_noncal
from abinitostudio.ui.UI_vasp_DOS import Ui_Form_UI_vasp_DOS
from abinitostudio.ui.UI_vasp_phonon import Ui_Form_UI_vasp_phonon
from abinitostudio.ui.UI_vasp_wannier import Ui_Form_UI_vasp_wannier
from abinitostudio.ui.UI_vasp_supercell import Ui_Form_UI_supercell
from abinitostudio.calculation.vasp_calculation import *

from abinitostudio.io.vasp_io import readEIGENVAL,readDOSCAR,readPROCAR
from abinitostudio.plot.plot_vasp import plot_CHGCAR

# Global Variables

pos_path = ''


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.center()  # Window centering
        # Splitter control scale
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 1)
        self.ui.splitter_2.setStretchFactor(0, 3)
        self.ui.splitter_2.setStretchFactor(1, 2)
        # Mayavi window
        self.mayavi_widget = MayaviQWidget()  # Instantiate the MayaviQWidget class
        self.scene = self.mayavi_widget.visualization.scene
        self.ui.verticalLayout_2.addWidget(self.mayavi_widget)
        # Matplotlib drawing
        self.plt_pattern = Figure_Canvas(self, width=5, height=4, dpi=100)
        self.axes = self.plt_pattern.fig.add_subplot(111)
        self.plt_toolbar = NavigationToolbar(self.plt_pattern, self)

        self.__cid = self.plt_pattern.mpl_connect("scroll_event", self.do_scrollZoom)  # Mouse scrolling zoom
        self.ui.verticalLayout.addWidget(self.plt_toolbar)
        self.ui.verticalLayout.addWidget(self.plt_pattern)
        # Turn on drag-and-drop events
        self.setAcceptDrops(True)
        self.ui.textBrowser.setAcceptDrops(True)
        # Event response
        # File
        self.ui.actionvisual.triggered.connect(self.load_POSCAR)
        # Calculation_Pyxtal
        self.ui.actiontest.triggered.connect(self.test)
        # Calculation_VASP
        self.ui.actionscf.triggered.connect(lambda: self.calculation_vasp_interface('scf'))
        self.ui.actionscf_noncal.triggered.connect(lambda: self.vasp_interface('scf_noncal'))
        self.ui.actionbands.triggered.connect(lambda: self.vasp_interface('band'))
        self.ui.actionband_noncal.triggered.connect(lambda: self.vasp_interface('band_noncal'))
        self.ui.actionDOS.triggered.connect(lambda: self.vasp_interface('dos'))
        self.ui.actionphonon.triggered.connect(lambda: self.vasp_interface('phonon'))
        self.ui.actionwannier.triggered.connect(lambda: self.vasp_interface('wannier'))
        # Plot
        self.ui.actionband.triggered.connect(self.show_Dialog_bands)
        self.ui.actionprojectionband.triggered.connect(self.show_Dialog_PB)
        self.ui.actiondos.triggered.connect(self.show_Dialog_DOS)
        
        self.ui.actionchgcar.triggered.connect(lambda: self.plot_vasp_CHGCAR('CHGCAR'))
        # Tools
        self.ui.actionsupercell.triggered.connect(self.mayavi_widget.build_supercell)
        # Settings
        self.ui.actionsetting.triggered.connect(self.setting)
        # Help
        self.ui.actioninstruction.triggered.connect(self.instruction)
        self.ui.actionabout.triggered.connect(self.about)

        self.code_path = os.getcwd()

        self.have_connected = False
        self.get_ip_info = False

    # Drag events
    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            for url in e.mimeData().urls():
                self.ui.textBrowser.append(url.path()[1:] + "\n")
            filename = e.mimeData().urls()[0].path()[1:]
            full_path = url.path()[1:]
            basename, ext = os.path.splitext(os.path.basename(filename))
            print(basename)
            if basename == 'POSCAR':
                global pos_path
                pos_path = filename
                self.scene.scene_editor._tool_bar.setVisible(True)
                supercell = (1, 1, 1)
                plot_str(full_path, self.scene, supercell)
            # if basename[0:8] == 'EIGENVAL':
            #     self.filename = url.path()[1:]
            #     self.plat_bands()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                               'Are you sure you want to exit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            # sys.exit(app.exec_())
        else:
            event.ignore()

    # Test passing participation
    def test(self):
        self.dialog_test = Test_table()
        # get desktop path
        self.dialog_test.lineEdit.setText(os.path.join(os.path.expanduser('~'), "Desktop\\VASP_files"))
        # self.dialog_test.setModal(True)  # Set modal window
        self.dialog_test.show()
        self.dialog_test.pushButton.clicked.connect(self.pyxtal_func)
        self.ui.actionclose.triggered.connect(self.dialog_test.close)
        self.ui.textBrowser.append("A random structure have been produced.")
        self.dialog_test.exec_()

    # run test function
    def pyxtal_func(self):
        self.get_parm_pyxtal()
        my_crystal = pyxtal()
        path = self.path  # "C:\\Users\\Administrator\\Desktop"
        # my_crystal.from_random(2, 51, ['C', 'N'], [1, 3])
        my_crystal.from_random(self.dim, self.spa_group, self.ele_type, self.ele_num)
        ase_struc = my_crystal.to_ase()
        str_type = 'pos'
        filename = ''
        if str_type == 'pos':
            filename = path + '\\POSCAR'
            ase.io.vasp.write_vasp(filename, ase_struc, vasp5=True)
            # file_open = filename
        elif str_type == 'cif':
            filename = path + '\\case' + '.cif'
            ase_struc.write(filename, format='cif')
        self.load_POSCAR_direct()
        self.dialog_test.close()

    # get test parameter
    def get_parm_pyxtal(self):
        # If haven't this file directory, create a new one
        if not os.path.exists(self.dialog_test.lineEdit.text()):
            os.mkdir(self.dialog_test.lineEdit.text())
        self.path = self.dialog_test.lineEdit.text()  # 保存文件目录
        self.dim = int(self.dialog_test.lineEdit_2.text())  # 维度
        self.spa_group = int(self.dialog_test.lineEdit_3.text())  # 空间群
        self.ele_type = eval(self.dialog_test.lineEdit_4.text())  # 元素种类
        self.ele_num = eval(self.dialog_test.lineEdit_5.text())  # 元素数目
        self.thickness = self.dialog_test.lineEdit_6.text()  # Thickness

    # the POSCAR generated by test is opened directly
    def load_POSCAR_direct(self):
        self.scene.scene_editor._tool_bar.setVisible(True)
        supercell = (1, 1, 1)
        plot_str(self.path + "\\POSCAR", self.scene, supercell)

    # Bands
    def show_Dialog_bands(self):
        curPath = QDir.currentPath()  # Get the current directory of the system
        dlgTitle = "Choose a EIGENVAL file"  # Dialog title
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"  # File filters
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        # filename = 'E:\\python\\project_1\\my_project\\tooltik\\EIGENVAL'
        extractfileName = (os.path.basename(filename))[0:8]
        if extractfileName == "EIGENVAL":
            dialog = Bounced_bands()
            dialog.setModal(True)  # Set up modal windows
            dialog.show()

            def pB_OK():
                self.fermi_level = float(dialog.lineEdit.text())
                self.x_min_bands = float(dialog.lineEdit_2.text())
                self.y_min_bands = float(dialog.lineEdit_4.text())
                self.y_max_bands = float(dialog.lineEdit_5.text())
                self.y_label_bands = dialog.lineEdit_7.text()
                self.title_bands = dialog.lineEdit_8.text()
                self.dots_num_bands = int(dialog.lineEdit_9.text())
                self.load_EIGENVAL(filename)
                dialog.close()

            dialog.pushButton.clicked.connect(pB_OK)
            dialog.exec_()
        else:
            self.ui.textBrowser.setText("The file you choose is not a EIGENVAL file.")



    def load_EIGENVAL(self, fileName):
        self.axes.cla()  # empty the sketchpad
        eigfile_1 = readEIGENVAL(fileName)[1]
        nk, num_band = np.shape(eigfile_1)  # 180,32
        e_tmp = np.array(
            eigfile_1).T  # e_tmp is a multi-dimensional array, it has 32 dimensions (number of energy bands), each dimension is from 0 to 240 (horizontal coordinates)
        self.x_max_bands = len(e_tmp[0])  # Horizontal coordinate maximum 240
        self.period_dots_num = len(e_tmp[0]) / (self.dots_num_bands)
        xticks = []
        for i in range(self.dots_num_bands):
            self.axes.axvline(x=i * self.period_dots_num, ls=":", c="black")  # Add vertical line
            xticks.append(int(i * self.period_dots_num))
        xticks.append(int(self.x_max_bands))
        self.axes.set_xticks([])  # Do not show x-coordinate
        self.axes.set_xticks(xticks)
        self.axes.axhline(y=0, ls=":", c="black")  # Add horizontal line
        self.axes.set_xlim(self.x_min_bands, self.x_max_bands)
        self.axes.set_ylim(self.y_min_bands, self.y_max_bands)
        self.axes.set(xlabel="", ylabel=self.y_label_bands, title=self.title_bands)
        for i in range(num_band):  # num_band is the number of energy bands of 32
            self.axes.plot((e_tmp[i]) - (self.fermi_level), c='b')
        if readEIGENVAL(fileName)[0] == 3:
            eigfile_2 = readEIGENVAL(fileName)[2]
            e_tmp_2 = np.array(eigfile_2).T
            for i in range(num_band):  # num_band is the number of energy bands of 32
                self.axes.plot((e_tmp_2[i]) - (self.fermi_level), c='r')
            self.axes.plot((e_tmp[0]) - (self.fermi_level), c='b', label='$spin-up$')
            self.axes.plot((e_tmp_2[0]) - (self.fermi_level), c='r', label='$spin-down$')
        self.ui.textBrowser.setText(f"\nThe number of bands：{len(e_tmp)}\n")
        self.ui.textBrowser.append(f"\n you open a EIGENVAL file, the path is：\n{fileName}")
        self.plt_pattern.draw()  # refresh the palette to draw

    # Projection bands
    def show_Dialog_PB(self):
        curPath = QDir.currentPath()  # Get system current directory
        dlgTitle = "选择一个PROCAR文件"  # Dialog title
        filt = "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg *.gif *.png)"  # File filter
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "PROCAR":
            dialog = Bounced_PB()
            dialog.setModal(True)  # Set modal window
            dialog.show()
            self.color_sum = "#0055ff"

            self.color_s = "#0055ff"
            self.color_p = "#ff0000"
            self.color_d = "#00aa00"
            self.color_tol = "#5500ff"

            self.color_p_y = "#aa5500"
            self.color_p_z = "#aa55ff"
            self.color_p_x = "#ff5500"

            self.color_d_xy = "#ff557f"
            self.color_d_yz = "#55aa7f"
            self.color_d_z2 = "#aaaa7f"
            self.color_d_xz = "#ffaa7f"
            self.color_d_x2_y2 = "#ffff7f"

            def pB():
                # Passing parameters from a PB diglog
                self.fermi_level = float(dialog.lineEdit.text())
                self.high_point_num = int(dialog.lineEdit_16.text())
                self.y_min_pb = float(dialog.lineEdit_4.text())
                self.y_max_pb = float(dialog.lineEdit_5.text())
                self.y_label_pb = dialog.lineEdit_7.text()
                self.title_pb = dialog.lineEdit_8.text()
                self.ratio = float(dialog.lineEdit_9.text())
                self.listatom_input = dialog.lineEdit_12.text()
                self.atomname_atom = dialog.lineEdit_15.text()
                self.radioButton = dialog.radioButton

                self.state_s_pb = dialog.checkBox.checkState()
                self.state_p_tol_pb = dialog.checkBox_2.checkState()
                self.state_d_tol_pb = dialog.checkBox_3.checkState()
                self.state_tol_pb = dialog.checkBox_4.checkState()

                self.state_p_y_pb = dialog.checkBox_5.checkState()
                self.state_p_z_pb = dialog.checkBox_6.checkState()
                self.state_p_x_pb = dialog.checkBox_7.checkState()

                self.state_d_xy_pb = dialog.checkBox_8.checkState()
                self.state_d_yz_pb = dialog.checkBox_9.checkState()
                self.state_d_z2_pb = dialog.checkBox_10.checkState()
                self.state_d_xz_pb = dialog.checkBox_11.checkState()
                self.state_d_x2_y2_pb = dialog.checkBox_12.checkState()

                self.narrow = int(dialog.lineEdit_17.text())
                self.ion_orb_num = int(dialog.lineEdit_18.text())

                self.zorder_s = int(dialog.lineEdit_10.text())
                self.zorder_p_tol = int(dialog.lineEdit_11.text())
                self.zorder_d_tol = int(dialog.lineEdit_13.text())
                self.zorder_tol = int(dialog.lineEdit_14.text())
                self.zorder_p_y = int(dialog.lineEdit_19.text())
                self.zorder_p_z = int(dialog.lineEdit_20.text())
                self.zorder_p_x = int(dialog.lineEdit_21.text())
                self.zorder_d_xy = int(dialog.lineEdit_22.text())
                self.zorder_d_yz = int(dialog.lineEdit_23.text())
                self.zorder_d_z2 = int(dialog.lineEdit_24.text())
                self.zorder_d_xz = int(dialog.lineEdit_25.text())
                self.zorder_d_x2_y2 = int(dialog.lineEdit_26.text())
                # The function load_PROCAR is the actual drawing function
                self.load_PROCAR(filename)
                dialog.close()

            def Color_choose_s():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_s = self.color.name()
                dialog.pushButton_3.setStyleSheet('QPushButton {background-color:%s}' % self.color_s)

            def Color_choose_p():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p = self.color.name()
                dialog.pushButton_4.setStyleSheet('QPushButton {background-color:%s}' % self.color_p)

            def Color_choose_d():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d = self.color.name()
                dialog.pushButton_5.setStyleSheet('QPushButton {background-color:%s}' % self.color_d)

            def Color_choose_tol():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_tol = self.color.name()
                dialog.pushButton_6.setStyleSheet('QPushButton {background-color:%s}' % self.color_tol)

            def Color_choose_p_y():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_y = self.color.name()
                dialog.pushButton_7.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_y)

            def Color_choose_p_z():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_z = self.color.name()
                dialog.pushButton_8.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_z)

            def Color_choose_p_x():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_p_x = self.color.name()
                dialog.pushButton_9.setStyleSheet('QPushButton {background-color:%s}' % self.color_p_x)

            def Color_choose_d_xy():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_xy = self.color.name()
                dialog.pushButton_10.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_xy)

            def Color_choose_d_yz():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_yz = self.color.name()
                dialog.pushButton_11.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_yz)

            def Color_choose_d_z2():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_z2 = self.color.name()
                dialog.pushButton_12.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_z2)

            def Color_choose_d_xz():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_xz = self.color.name()
                dialog.pushButton_13.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_xz)

            def Color_choose_d_x2_y2():
                self.color = QColorDialog.getColor()  # QColor gets the current color
                self.color_d_x2_y2 = self.color.name()
                dialog.pushButton_14.setStyleSheet('QPushButton {background-color:%s}' % self.color_d_x2_y2)

            dialog.pushButton.clicked.connect(pB)
            # 传入颜色
            dialog.pushButton_2.clicked.connect(self.Color_choose)
            dialog.pushButton_3.clicked.connect(Color_choose_s)
            dialog.pushButton_4.clicked.connect(Color_choose_p)
            dialog.pushButton_5.clicked.connect(Color_choose_d)
            dialog.pushButton_6.clicked.connect(Color_choose_tol)
            dialog.pushButton_7.clicked.connect(Color_choose_p_y)
            dialog.pushButton_8.clicked.connect(Color_choose_p_z)
            dialog.pushButton_9.clicked.connect(Color_choose_p_x)
            dialog.pushButton_10.clicked.connect(Color_choose_d_xy)
            dialog.pushButton_11.clicked.connect(Color_choose_d_yz)
            dialog.pushButton_12.clicked.connect(Color_choose_d_z2)
            dialog.pushButton_13.clicked.connect(Color_choose_d_xz)
            dialog.pushButton_14.clicked.connect(Color_choose_d_x2_y2)
            self.ui.textBrowser.setText("投影能带绘制准备中...")
            dialog.exec_()
        else:
            self.ui.textBrowser.setText("你打开的不是一个PROCAR文件")



    def load_PROCAR(self, fileName):
        total_band_atom = readPROCAR(fileName)[0]
        k_x = readPROCAR(fileName)[1]  # 180个横坐标
        k_y = readPROCAR(fileName)[2]  # 180个纵坐标每个*16
        n_kpoints = readPROCAR(fileName)[3]  # k点数
        n_bands = readPROCAR(fileName)[4]  # 能带条数
        narrow = self.narrow  # 缩放因子
        ion_orb_num = self.ion_orb_num  # 原子轨道下标索引
        # print(total_band_atom)
        self.axes.cla()  # 清空画板
        # if self.radioButton.isChecked() == True:#是否分开绘制轨道
        # p
        if self.state_p_y_pb == 2:
            self.ui.textBrowser.append("\n选择了p_y轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    # print(len(k_x[i]),len(k_y[i][1]))
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][1]),
                                              marker='o', c=self.color_p_y, zorder=self.zorder_p_y)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10,
                                  c=self.color_p_y, label=self.atomname_atom + '$-p-y$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append("p_y轨道选择的颜色为：" + f"<font color={self.color_p_y}>{self.color_p_y}</font>\n")
        if self.state_p_z_pb == 2:
            self.ui.textBrowser.append("\n选择了p_z轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][2]),
                                              marker='o',
                                              c=self.color_p_z, zorder=self.zorder_p_z)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p_z, label=self.atomname_atom + '$-p-z$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "p_z轨道选择的颜色为：" + f"<font color={self.color_p_z}>{self.color_p_z}</font>\n")
        if self.state_p_x_pb == 2:
            self.ui.textBrowser.append("\n选择了p_x轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][3]),
                                              marker='o', c=self.color_p_x, zorder=self.zorder_p_x)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p_x, label=self.atomname_atom + '$-p-x$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "p_x轨道选择的颜色为：" + f"<font color={self.color_p_x}>{self.color_p_x}</font>\n")
        # d
        if self.state_d_xy_pb == 2:
            self.ui.textBrowser.append("\n选择了d_xy轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][4]),
                                              marker='o', c=self.color_d_xy, zorder=self.zorder_d_xy)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_xy, label=self.atomname_atom + '$-d-xy$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d_xy轨道选择的颜色为：" + f"<font color={self.color_d_xy}>{self.color_d_xy}</font>\n")
        if self.state_d_yz_pb == 2:
            self.ui.textBrowser.append("\n选择了d_yz轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][5]),
                                              marker='o', c=self.color_d_yz, zorder=self.zorder_d_yz)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_yz, label=self.atomname_atom + '$-d-yz$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d_yz轨道选择的颜色为：" + f"<font color={self.color_d_yz}>{self.color_d_yz}</font>\n")
        if self.state_d_z2_pb == 2:
            self.ui.textBrowser.append("\n选择了d_z2轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][6]),
                                              marker='o', c=self.color_d_z2, zorder=self.zorder_d_z2)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_z2, label=self.atomname_atom + '$-d-z2$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d_z2轨道选择的颜色为：" + f"<font color={self.color_d_z2}>{self.color_d_z2}</font>\n")
        if self.state_d_xz_pb == 2:
            self.ui.textBrowser.append("\n选择了d_xz轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][7]),
                                              marker='o', c=self.color_d_xz, zorder=self.zorder_d_xz)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_xz, label=self.atomname_atom + '$-d-xz$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d_xz轨道选择的颜色为：" + f"<font color={self.color_d_xz}>{self.color_d_xz}</font>\n")
        if self.state_d_x2_y2_pb == 2:
            self.ui.textBrowser.append("\n选择了d_x2_y2轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][8]),
                                              marker='o', c=self.color_d_x2_y2, zorder=self.zorder_d_x2_y2)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d_x2_y2, label=self.atomname_atom + '$-d-x2-y2$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d_x2_y2轨道选择的颜色为：" + f"<font color={self.color_d_x2_y2}>{self.color_d_x2_y2}</font>\n")
        # total
        if self.state_s_pb == 2:
            self.ui.textBrowser.append("\n选择了s轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][0]),
                                              marker='o', c=self.color_s, zorder=self.zorder_s)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_s, label=self.atomname_atom + '$-s$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "s轨道选择的颜色为：" + f"<font color={self.color_s}>{self.color_s}</font>\n")
        if self.state_p_tol_pb == 2:
            self.ui.textBrowser.append("\n选择了p轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][1] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][2] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][3]),
                                              marker='o', c=self.color_p, zorder=self.zorder_p_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_p, label=self.atomname_atom + '$-p-tol$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "p轨道选择的颜色为：" + f"<font color={self.color_p}>{self.color_p}</font>\n")
        if self.state_d_tol_pb == 2:
            self.ui.textBrowser.append("\n选择了d轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][4] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][5] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][6] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][7] +
                                                  total_band_atom[i * narrow][j][ion_orb_num][8]),
                                              marker='o', c=self.color_d, zorder=self.zorder_d_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_d, label=self.atomname_atom + '$-d-tol$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "d轨道选择的颜色为：" + f"<font color={self.color_d}>{self.color_d}</font>\n")
        if self.state_tol_pb == 2:
            self.ui.textBrowser.append("\n选择了total轨道")

            def threadFunc():
                for i in range(int(n_kpoints // narrow)):  # 循环180个k点
                    for j in range(n_bands):  # 每一个k点有16条能带
                        if self.y_min_pb < (k_y[i * narrow][j]) - self.fermi_level < self.y_max_pb:  # 多余的点不画出来
                            # total_band_atom[第1个k点][第1条能带][第1个原子][s轨道]
                            self.axes.scatter(k_x[i * narrow], k_y[i * narrow][j] - self.fermi_level,
                                              s=self.ratio * np.absolute(
                                                  total_band_atom[i * narrow][j][ion_orb_num][9]),
                                              marker='o', c=self.color_tol, zorder=self.zorder_tol)

                self.axes.scatter(k_x[-1], k_y[-1][-1] - self.fermi_level,
                                  s=10, c=self.color_tol, label=self.atomname_atom + '$-total$')
                self.axes.legend()  # 自动生成图例
                self.plt_pattern.draw()

            thread = Thread(target=threadFunc, args=())
            thread.start()
            self.ui.textBrowser.append(
                "total轨道选择的颜色为：" + f"<font color={self.color_tol}>{self.color_tol}</font>\n")

        """图例设置"""
        # 问题1，自动生成图例，隔一段时间自动刷新
        # 问题2，图层问题，比较贡献值 先p后d，先p后s
        # self.axes.legend()  # 自动生成图例
        self.axes.set_title(self.title_pb)  # 图片标题
        self.axes.set_xlim(0, max(k_x))
        self.axes.set_ylim(self.y_min_pb, self.y_max_pb)
        self.axes.set_xticks([])  # 不显示x坐标
        self.period_dots_num = int(len(k_x) / (self.high_point_num))  # 180/3=60
        for i in range(self.high_point_num):
            if i != 0:
                x = k_x[i * self.period_dots_num - 1]
                self.axes.axvline(x, ls=":", c="black")  # 添加垂直直线
        self.axes.axhline(y=0, ls=":", c="black")  # 添加水平直线
        self.plt_pattern.draw()

        # 态密度

    # Density of states
    def show_Dialog_DOS(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        dlgTitle = "选择一个DOSCAR文件"  # 对话框标题
        filt = "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg *.gif *.png)"  # 文件过滤器
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "DOSCAR":
            dialog = Bounced_DOS()
            dialog.setModal(True)  # 设置模态窗口
            dialog.show()

            def pB_OK():
                self.x_label_dos = dialog.lineEdit_5.text()
                self.y_label_dos = dialog.lineEdit_6.text()
                self.title_dos = dialog.lineEdit_7.text()
                self.state_tol_DOS = dialog.checkBox_2.checkState()
                self.state_up_DOS = dialog.checkBox_3.checkState()
                self.state_down_DOS = dialog.checkBox_15.checkState()
                self.state_s_DOS = dialog.checkBox_4.checkState()
                self.state_p_tol_DOS = dialog.checkBox_5.checkState()
                self.state_d_tol_DOS = dialog.checkBox_6.checkState()
                self.state_p_y_DOS = dialog.checkBox_7.checkState()
                self.state_p_z_DOS = dialog.checkBox_8.checkState()
                self.state_p_x_DOS = dialog.checkBox_9.checkState()
                self.state_d_xy_DOS = dialog.checkBox_10.checkState()
                self.state_d_yz_DOS = dialog.checkBox_11.checkState()
                self.state_d_z2_DOS = dialog.checkBox_12.checkState()
                self.state_d_xz_DOS = dialog.checkBox_13.checkState()
                self.state_d_x2_y2_DOS = dialog.checkBox_14.checkState()

                self.load_DOSCAR(filename)
                dialog.close()

            dialog.pushButton.clicked.connect(pB_OK)
            dialog.exec_()
        else:
            self.ui.textBrowser.setText("你打开的不是一个DOSCAR文件")


    def load_DOSCAR(self, fileName):
        self.axes.cla()  # empty the sketchpad
        #
        dosfile = readDOSCAR(fileName, 0)  # dosfile是一个列表,len(dosfile)=5
        nepoint = np.shape(dosfile[0])[0]  # nepoint是一个数=301，dosfile[0]是numpy.ndarray
        x_dos = dosfile[0]
        y_dos_t = dosfile[1]
        y_dos_i = dosfile[2]
        y_dos_s = dosfile[3]
        y_dos_py = dosfile[4]
        y_dos_pz = dosfile[5]
        y_dos_px = dosfile[6]
        y_dos_p_tol = y_dos_py + y_dos_pz + y_dos_px
        y_dos_d_xy = dosfile[7]
        y_dos_d_yz = dosfile[8]
        y_dos_d_z2 = dosfile[9]
        y_dos_d_xz = dosfile[10]
        y_dos_d_x2_y2 = dosfile[11]
        y_dos_d_tol = y_dos_d_xy + y_dos_d_yz + y_dos_d_z2 + y_dos_d_xz + y_dos_d_x2_y2
        y_tol = y_dos_s + y_dos_p_tol + y_dos_d_tol

        self.x_min_dos = min(x_dos)
        self.x_max_dos = max(x_dos)
        self.y_min_dos = min(y_dos_t)
        self.y_max_dos = (max(y_dos_t)) * 1.1

        # s
        if self.state_s_DOS == 2:
            self.y_max_dos = (max(y_dos_s)) * 1.1
            self.axes.plot(x_dos, y_dos_s, label='$s-DOS$')
        # p
        if self.state_p_y_DOS == 2:
            self.y_max_dos = (max(y_dos_py)) * 1.1
            self.axes.plot(x_dos, y_dos_py, label='$p-y-DOS$')
        if self.state_p_z_DOS == 2:
            self.y_max_dos = (max(y_dos_pz)) * 1.1
            self.axes.plot(x_dos, y_dos_pz, label='$p-z-DOS$')
        if self.state_p_x_DOS == 2:
            self.y_max_dos = (max(y_dos_px)) * 1.1
            self.axes.plot(x_dos, y_dos_px, label='$p-x-DOS$')
        if self.state_p_tol_DOS == 2:
            self.y_max_dos = (max(y_dos_p_tol)) * 1.1
            self.axes.plot(x_dos, y_dos_p_tol, label='$p-tol-DOS$')
        # d
        if self.state_d_xy_DOS == 2:
            self.y_max_dos = (max(y_dos_d_xy)) * 1.1
            self.axes.plot(x_dos, y_dos_d_xy, label='$d-xy-DOS$')
        if self.state_d_yz_DOS == 2:
            self.y_max_dos = (max(y_dos_d_yz)) * 1.1
            self.axes.plot(x_dos, y_dos_d_yz, label='$d-yz-DOS$')
        if self.state_d_z2_DOS == 2:
            self.y_max_dos = (max(y_dos_d_z2)) * 1.1
            self.axes.plot(x_dos, y_dos_d_z2, label='$d-z2-DOS$')
        if self.state_d_xz_DOS == 2:
            self.y_max_dos = (max(y_dos_d_xz)) * 1.1
            self.axes.plot(x_dos, y_dos_d_xz, label='$d-xz-DOS$')
        if self.state_d_x2_y2_DOS == 2:
            self.y_max_dos = (max(y_dos_d_x2_y2)) * 1.1
            self.axes.plot(x_dos, y_dos_d_x2_y2, label='$d-x2-y2-DOS$')
        if self.state_d_tol_DOS == 2:
            self.y_max_dos = (max(y_dos_p_tol)) * 1.1
            self.axes.plot(x_dos, y_dos_d_tol, label='$d-tol-DOS$')
        # tol
        if self.state_tol_DOS == 2:
            self.y_max_dos = (max(y_tol)) * 1.1
            self.axes.plot(x_dos, y_tol, label='$tol-DOS$')
        if self.state_up_DOS == 2:
            self.y_max_dos = (max(y_dos_t)) * 1.1
            self.axes.plot(x_dos, y_dos_t, label='$up-DOS$')
        if self.state_down_DOS == 2:
            self.y_max_dos = (max(y_dos_i)) * 1.1
            self.axes.plot(x_dos, y_dos_i, label='$down-DOS$')
        self.axes.set_xlim(self.x_min_dos, self.x_max_dos)
        self.axes.set_ylim(self.y_min_dos, self.y_max_dos)
        self.axes.set(xlabel=self.x_label_dos, ylabel=self.y_label_dos,
                      title=self.title_dos)
        #
        # self.ui.verticalLayout.addWidget(self.plt_toolbar)
        # self.ui.verticalLayout.addWidget(self.plt_pattern)  # 把plt_patt# Put plt_pattern into splitter 1ern放进分割器1
        self.ui.textBrowser.setText(f"X最小值：{self.x_min_dos}\nX最大值：{self.x_max_dos}\n"
                                    f"Y最小值：{self.y_min_dos}\nY最大值：{(self.y_max_dos) / 1.1}")
        self.ui.textBrowser.append(f"\n打开了DOSCAR文件，路径为：\n {fileName}")
        self.plt_pattern.draw()  # refresh the palette to draw

    # 3D atomic structure
    def load_POSCAR(self):
        curPath = QDir.currentPath()  # Get the current directory of the system
        dlgTitle = "Choose a POSCAR"  # Dialog title
        filt = "All files(*.*);; Text files(*.txt);;figure files(*.jpg *.gif *.png)"  # File filters
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        global pos_path
        pos_path = filename
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "POSCAR":
            self.scene.scene_editor._tool_bar.setVisible(True)
            supercell = (1, 1, 1)
            plot_str(filename, self.scene, supercell)

    def get_ip_information(self):
        if os.path.exists('node_information.txt'):
            cfile = open('node_information.txt', 'r')
            lines = cfile.readlines()

            ip_info = {}
            for i in range(len(lines)):
                tmpArr = lines[i].split(':')
                # print(tmpArr)
                if tmpArr[0].strip() == 'jump':
                    ip_info['jump'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_ip':
                    ip_info['jump_ip'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_username':
                    ip_info['jump_username'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'jump_password':
                    ip_info['jump_password'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_ip':
                    ip_info['cal_ip'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_username':
                    ip_info['cal_username'] = tmpArr[1].strip()
                elif tmpArr[0].strip() == 'cal_password':
                    ip_info['cal_password'] = tmpArr[1].strip()

            # print(ip_info)
            cfile.close()
        else:
            ip_info = None
        # ip_info = {'jump': True, 'jump_ip': '202.197.234.194', 'jump_username': 'zhoupan',
        #            'jump_password': 'zhoupan123', 'cal_ip': '192.168.1.4', 'cal_username': 'zhoupan',
        #            'cal_password': 'zhoupan123'}
        return ip_info

    # Setting
    def setting(self):
        ip_info = self.get_ip_information()
        self.dialog_setting = Setting_table()
        # get desktop path
        self.dialog_setting.lineEdit_5.setText(os.path.join(os.path.expanduser('~'), "Desktop", "VASP_files"))
        self.dialog_setting.lineEdit_4.setText('/home/zhoupan/zhoupan')

        def get_text_info():
            self.dialog_setting.lineEdit_6.setText(ip_info['jump_ip'])
            self.dialog_setting.lineEdit_8.setText(ip_info['jump_username'])
            self.dialog_setting.lineEdit_7.setText(ip_info['jump_password'])
            self.dialog_setting.lineEdit.setText(ip_info['cal_ip'])
            self.dialog_setting.lineEdit_2.setText(ip_info['cal_username'])
            self.dialog_setting.lineEdit_3.setText(ip_info['cal_password'])

        # dialog.setModal(True)  # Set modal window
        self.dialog_setting.show()
        self.dialog_setting.pushButton.clicked.connect(self.setting_func)
        if ip_info != None:
            self.dialog_setting.pushButton_2.clicked.connect(get_text_info)
        else:
            self.ui.textBrowser.append(
                'node_information.txt can\'t be found. Please input the node information manually!!!')
        self.ui.actionclose.triggered.connect(self.dialog_setting.close)
        self.dialog_setting.exec_()

    # run setting function
    def setting_func(self):
        self.setting_parameter()
        if self.dialog_setting.checkBox.checkState() == 2:
            try:
                self.gateway_session = SSHSession(self.jumpnodeip,
                                                  username=self.jumpnodeuser,
                                                  password=self.jumpnodepass).open()
                self.remote_session = self.gateway_session.get_remote_session(self.nodeip,
                                                                              username=self.nodeuser,
                                                                              password=self.nodepass)
            except:
                self.warning_2()
        else:
            try:
                self.remote_session = SSHSession(self.nodeip,
                                                 username=self.nodeuser,
                                                 password=self.nodepass).open()
                self.ui.textBrowser.append("Node connection successful.")
            except:
                self.ui.textBrowser.append("Node connection failed.")
                self.warning_2()

        self.get_ip_info = True
        # print(self.nodeip)
        # print(self.nodeuser)
        # print(self.nodepass)
        # print(self.nodepath)
        # print(self.local_path)
        # print("")

    # get setting parameter
    def setting_parameter(self):
        # Node Info
        self.nodeip = self.dialog_setting.lineEdit.text()  # node ip
        self.nodeuser = self.dialog_setting.lineEdit_2.text()  # node user name
        self.nodepass = self.dialog_setting.lineEdit_3.text()  # node password
        self.nodepath = self.dialog_setting.lineEdit_4.text()  # node path
        # Jump Node Info
        self.jumpnodeip = self.dialog_setting.lineEdit_6.text()  # jump ip
        self.jumpnodeuser = self.dialog_setting.lineEdit_8.text()  # jump user name
        self.jumpnodepass = self.dialog_setting.lineEdit_7.text()  # jump password
        # Local Info
        self.local_path = self.dialog_setting.lineEdit_5.text()  # win local path
        # If haven't this file directory, create a new one
        if not os.path.exists(self.local_path):
            os.mkdir(self.local_path)
        # run function
        if self.dialog_setting.checkBox.checkState() == 2:
            self.ui.textBrowser.append("A jump server is used!!")
        self.dialog_setting.close()

    def calculation_vasp_interface(self, cal_type):
        if self.get_ip_info:
            vasp_cal = vasp_calculation()
            vasp_cal.set_output(self.ui.textBrowser)

            vasp_cal.set_connection(self.remote_session, self.get_ip_info)
            vasp_cal.set_path(self.local_path, self.nodepath, self.code_path)

            if cal_type == 'scf':
                vasp_cal.vasp_scf()
            elif cal_type == 'band':
                vasp_cal.vasp_band()
            elif cal_type == 'scf_noncal':
                vasp_cal.vasp_scf_noncal()
            elif cal_type == 'band_noncal':
                vasp_cal.vasp_band_noncal()
            elif cal_type == 'wannier':
                vasp_cal.vasp_wannier()
            elif cal_type == 'phonon':
                vasp_cal.vasp_phonon()

        else:
            self.warning_1()
            
    def plot_vasp_CHGCAR(self, file_type):
        curPath = QDir.currentPath()  # Get the current directory of the system
        dlgTitle = "Choose a CHGCAR file"  # Dialog title
        filt = "All files(*.*);;Text file(*.txt);;figure file(*.jpg *.gif *.png)"  # File filters
        filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        # filename = 'E:\\python\\project_1\\my_project\\tooltik\\CHGCAR'
        extractfileName = (os.path.basename(filename))[0:6]
        if file_type == 'CHGCAR':
            plot_CHGCAR(filename, self.scene)
            self.ui.textBrowser.append(f"\n You open a CHGCAR file, the path is：\n{filename}")

    # Instruction
    def instruction(self):
        dlgTitle = "Instruction"
        strInfo = "Version: 1.0\n\n" \
                  "The three functions of Band, DOS, and Projected Band are provided temporarily." \
                  "\n\nPlease look forward to other functions."
        QMessageBox.information(self, dlgTitle, strInfo)

    # About
    def about(self):
        dlgTitle = "About"
        strInfo = "Abinito Studio 1.0\n\n" \
                  "The developer has made every effort to ensure the accuracy of this software, but inevitably there will be omissions. " \
                  "You are welcome to give us feedback on the problems you find to help us improve the quality of the software.\n\n" \
                  "QQ group number: 461248214"
        QMessageBox.information(self, dlgTitle, strInfo)  # about


    # Zoom by mouse wheel
    def do_scrollZoom(self, event):
        ax = event.inaxes  # Generate event axes objects
        if ax == None:
            return

        self.plt_toolbar.push_current()  # Push the current view limits and position onto the stack，this is the way to restore.
        xmin, xmax = ax.get_xbound()
        xlen = xmax - xmin
        ymin, ymax = ax.get_ybound()
        ylen = ymax - ymin

        xchg = event.step * xlen / 20  # step [scalar],positive = ’up’, negative ='down'
        xmin = xmin + xchg
        xmax = xmax - xchg
        ychg = event.step * ylen / 20
        ymin = ymin + ychg
        ymax = ymax - ychg

        ax.set_xbound(xmin, xmax)
        ax.set_ybound(ymin, ymax)
        event.canvas.draw()

    # Color selection
    def Color_choose(self):
        self.color = QColorDialog.getColor()  # QColor gets the current color
        self.color_sum = self.color.name()

    # Center the main window
    def center(self):
        # Get screen coordinates
        screen = QDesktopWidget().screenGeometry()
        # Get window coordinates
        size = self.geometry()
        # Main window width and height
        width = 800
        height = 550
        self.resize(width, height)
        newLeft = (screen.width() - size.width() - (width / 2)) / 2
        newTop = (screen.height() - size.height() - (height / 2)) / 2
        self.move(newLeft, newTop)

    def warning_1(self):
        dlgTitle = "Warning"
        strInfo = "Please set the information about the node！"
        QMessageBox.warning(self, dlgTitle, strInfo)

    def warning_2(self):
        dlgTitle = "Warning"
        strInfo = "Remote connection failed.\n" \
                  "Please check the node information input!"
        QMessageBox.warning(self, dlgTitle, strInfo)


class Figure_Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=100)
        super(Figure_Canvas, self).__init__(self.fig)
        self.setParent(parent)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # Chinese font setting - bold
        plt.rcParams[
            'axes.unicode_minus'] = False  # Resolves the problem of saving images with a negative '-' sign displayed as a block


# Middle mayavi window
class MayaviQWidget(QWidget):  # Mayavi window
    def __init__(self, parent=None):  # Initialization
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)  # Vertical layout
        layout.setContentsMargins(0, 0, 0,
                                  0)  # Content margin, the distance from the control to the four surrounding edges (left, top, right, bottom)
        layout.setSpacing(0)  # The distance between the top and bottom of the control and the form
        self.visualization = Visualization()  # Visualization
        self.ui = self.visualization.edit_traits(parent=self, kind='subpanel').control
        layout.addWidget(self.ui)  # Add self.ui to the layout, which is a vertical layout
        self.ui.setParent(self)  # Parent window fis itself

    # Build_supercell
    def build_supercell(self):  # Build super cell
        # curPath = QDir.currentPath()  # Get the current directory of the system
        # dlgTitle = "选择一个POSCAR文件"  # Dialog title
        # filt = "所有文件(*.*);;文本文件(*.txt);;图片文件(*.jpg *.gif *.png)"  # File filters
        # filename, filtUsed = QFileDialog.getOpenFileName(self, dlgTitle, curPath, filt)
        filename = pos_path
        extractfileName = (os.path.basename(filename))[0:6]
        if extractfileName == "POSCAR":
            superdia = TabDialog(filename, self.visualization.scene)  # Label Dialog
            superdia.exec_()  # Ensure a clean exit of the application


# Scientific Computing 3D Visualization - Listening of Traits Properties
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')  # Scientific Computing 3D Visualization - Listening for Traits Attributes
    def update_plot(self):
        self.scene.mlab.clf()  # Clear the current scene
        self.scene.background = (1, 1, 1)
        self.scene.parallel_projection = True

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True  # The height and width of the middle Mayavi window
                )


# Parameter Input Dialog
class Test_table(QDialog, Ui_Form_UI_test):
    def __init__(self):
        super(Test_table, self).__init__()
        self.setupUi(self)


# Setting Input Dialog
class Setting_table(QDialog, Ui_Form_UI_setting):
    def __init__(self):
        super(Setting_table, self).__init__()
        self.setupUi(self)
        self.resize(1000, 500)


# Bands Dialog
class Bounced_bands(QtWidgets.QDialog, Ui_Dialog_band):
    def __init__(self):
        super(Bounced_bands, self).__init__()
        self.setupUi(self)


# Projection Bands Dialog
class Bounced_PB(QtWidgets.QDialog, Ui_Dialog_PB):
    def __init__(self):
        super(Bounced_PB, self).__init__()
        self.setupUi(self)


# DOS Dialog
class Bounced_DOS(QtWidgets.QDialog, Ui_Dialog_DOS):
    def __init__(self):
        super(Bounced_DOS, self).__init__()
        self.setupUi(self)


# Supercell Dialog
class Supercell_Dialog(QtWidgets.QDialog, Ui_Form_UI_supercell):
    def __init__(self):
        super(Supercell_Dialog, self).__init__()
        self.setupUi(self)


