# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:22:39 2021

@author: zhoup
"""
import sys
import os
from PyQt5.QtWidgets import QDialog, QApplication
from abinitostudio.ui.Dialog_DOS import Ui_Dialog_DOS
from abinitostudio.ui.Dialog_PB import Ui_Dialog_PB
from abinitostudio.ui.Dialog_band import Ui_Dialog_band
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


# Setting VASP Dialog
class Vasp_table_scf(QDialog, Ui_Form_UI_vasp_scf):
    def __init__(self):
        super(Vasp_table_scf, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_scf_noncal(QDialog, Ui_Form_UI_vasp_scf_noncal):
    def __init__(self):
        super(Vasp_table_scf_noncal, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_band(QDialog, Ui_Form_UI_vasp_band):
    def __init__(self):
        super(Vasp_table_band, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_band_noncal(QDialog, Ui_Form_UI_vasp_band_noncal):
    def __init__(self):
        super(Vasp_table_band_noncal, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_DOS(QDialog, Ui_Form_UI_vasp_DOS):
    def __init__(self):
        super(Vasp_table_DOS, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_phonon(QDialog, Ui_Form_UI_vasp_phonon):
    def __init__(self):
        super(Vasp_table_phonon, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class Vasp_table_wannier(QDialog, Ui_Form_UI_vasp_wannier):
    def __init__(self):
        super(Vasp_table_wannier, self).__init__()
        self.setupUi(self)
        self.resize(1500, 1000)


class vasp_calculation():
    def __init__(self):

        self.remote_session = None
        self.output = None
        self.local_path = None
        self.node_path = None
        self.scf_relax = False
        self.get_ip_info = None
        self.code_path = None
        self.tran_cal_vasp = False

    def set_output(self, text_output):
        self.output = text_output

    def set_connection(self, remote_node, have_connected):
        self.remote_session = remote_node
        self.get_ip_info = have_connected

    def set_path(self, local, node, code):
        self.local_path = local
        self.node_path = node
        self.code_path = code

    def write_file_vasp(self, filename, filetext):
        with open(filename, 'w') as f:
            f.write(filetext)

    def transport_file(self, filename):
        file_path = self.local_path + '\\' + filename
        des = self.node_path + '/' + filename
        self.remote_session.put(file_path, des)

    def transport_pos(self):
        # transport file POSCAR
        try:
            self.transport_file('POSCAR')
        except:
            self.output.append("POSCAR can't be found or tranported!!")
            sys.exit()

    def transport_cal_vasp(self):
        # transport file cal_vasp_single.py
        program_dir = 'pylib'
        code_path = self.code_path
        py_path = os.path.join(code_path, program_dir)
        file_path_cal_vasp_single = py_path + r'\cal_vasp_single.py'
        des_cal_vasp_single = self.node_path + r'/cal_vasp_single.py'
        self.remote_session.put(file_path_cal_vasp_single, des_cal_vasp_single)
        self.tran_cal_vasp = True

    def scf_calculation(self):
        if not self.tran_cal_vasp:
            self.transport_cal_vasp()

        # Change current working directory to self.local_path
        os.chdir(self.local_path)
        if self.scf_relax:
            self.write_file_vasp('INCAR_relax', self.rel_INCAR)
            self.transport_file('INCAR_relax')
            self.write_file_vasp('KPOINTS_relax', self.rel_KPOINTS)
            self.transport_file('KPOINTS_relax')

        # scf
        self.write_file_vasp('INCAR_scf', self.scf_INCAR)
        self.transport_file('INCAR_scf')
        self.write_file_vasp('KPOINTS_scf', self.scf_KPOINTS)
        self.transport_file('KPOINTS_scf')

        order1 = 'cd ' + self.node_path + '; '
        order2 = "python cal_vasp_single.py "
        order_npr = 'npr=' + self.np_wannier + ' '
        order_vasp = 'vasp=' + self.vasp_order + ' '
        order_psdir = 'psdir=' + self.POTCAR_path + ' '
        order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
        order_caldir = "cal_dir=" + self.cal_path_name + ' '
        if self.scf_relax:
            order3 = 'relax=1 scf=1 '
        else:
            order3 = 'scf=1'
        order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
        # print(order_all)
        self.output.append("The calculation is started")
        QApplication.processEvents()
        self.remote_session.run_cmd(order_all)
        self.output.append("The calculation is ended")
        QApplication.processEvents()

        if not os.path.exists(os.path.join(self.local_path, "scf")):
            os.mkdir(os.path.join(self.local_path, "scf"))
        eigfile = self.node_path + '/' + self.cal_path_name + '/scf/CHGCAR'
        print(eigfile)
        win = self.local_path + '\\scf\\' + 'CHGCAR'

        self.remote_session.get(remote_path=eigfile, local_path=win)
        self.output.append("Task completed, vasp_scf file returned")
        QApplication.processEvents()

        # Vasp

    def vasp_scf(self):
        dialog_vasp_scf = Vasp_table_scf()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_scf.show()
        if dialog_vasp_scf.checkBox.checkState() == 2:
            self.scf_relax = True

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR = dialog_vasp_scf.textEdit.toPlainText()
            self.rel_KPOINTS = dialog_vasp_scf.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = dialog_vasp_scf.textEdit_13.toPlainText()
            self.scf_KPOINTS = dialog_vasp_scf.textEdit_14.toPlainText()
            #
            self.POTCAR_path = dialog_vasp_scf.lineEdit.text()
            self.elements = dialog_vasp_scf.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_scf.lineEdit_3.text()
            self.vasp_order = dialog_vasp_scf.lineEdit_4.text()
            self.np_wannier = dialog_vasp_scf.lineEdit_5.text()

            # judge relax
            if self.scf_relax:
                print("结构优化")
            else:
                print("不需要结构优化")
            # run function
            # 这个位置写事件
            pass
            dialog_vasp_scf.close()
            self.output.append("Sent vasp_scf task")
            QApplication.processEvents()

        dialog_vasp_scf.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_scf.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_scf.pushButton_2.clicked.connect(self.scf_calculation)
        dialog_vasp_scf.exec_()

    def band_calculation(self):
        if not self.tran_cal_vasp:
            self.transport_cal_vasp()
        # Change current working directory to self.local_path
        os.chdir(self.local_path)
        # Writing VASP files and transport files
        if self.scf_relax:  # relax is or not True
            self.write_file_vasp('INCAR_relax', self.rel_INCAR)
            self.transport_file('INCAR_relax')
            self.write_file_vasp('KPOINTS_relax', self.rel_KPOINTS)
            self.transport_file('KPOINTS_relax')

        # scf
        self.write_file_vasp('INCAR_scf', self.scf_INCAR)
        self.transport_file('INCAR_scf')
        self.write_file_vasp('KPOINTS_scf', self.scf_KPOINTS)
        self.transport_file('KPOINTS_scf')
        # band
        self.write_file_vasp('INCAR_band', self.band_INCAR)
        self.transport_file('INCAR_band')
        self.write_file_vasp('KPOINTS_band', self.band_KPOINTS)
        self.transport_file('KPOINTS_band')

        order1 = 'cd ' + self.node_path + '; '
        order2 = "python cal_vasp_single.py "
        order_npr = 'npr=' + self.np_wannier + ' '
        order_vasp = 'vasp=' + self.vasp_order + ' '
        order_psdir = 'psdir=' + self.POTCAR_path + ' '
        order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
        order_caldir = "cal_dir=" + self.cal_path_name + ' '
        if self.scf_relax:
            order3 = 'relax=1 scf=1 band=1'
        else:
            order3 = 'scf=1 band=1'
        order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
        self.output.append("The calculation is started")
        QApplication.processEvents()
        self.remote_session.run_cmd(order_all)
        self.output.append("The calculation is ended")
        QApplication.processEvents()

        if not os.path.exists(os.path.join(self.local_path, "band")):
            os.mkdir(os.path.join(self.local_path, "band"))
        eigfile = self.node_path + '/' + self.cal_path_name + '/band/EIGENVAL'
        win = self.local_path + '\\band\\' + 'EIGENVAL'
        print(eigfile, win)
        self.remote_session.get(remote_path=eigfile, local_path=win)
        self.output.append("Task completed, vasp_band file returned")
        QApplication.processEvents()

    def vasp_band(self):
        dialog_vasp_band = Vasp_table_band()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_band.show()

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR = dialog_vasp_band.textEdit.toPlainText()
            self.rel_KPOINTS = dialog_vasp_band.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = dialog_vasp_band.textEdit_13.toPlainText()
            self.scf_KPOINTS = dialog_vasp_band.textEdit_14.toPlainText()
            # band
            self.band_INCAR = dialog_vasp_band.textEdit_19.toPlainText()
            self.band_KPOINTS = dialog_vasp_band.textEdit_20.toPlainText()
            #
            self.POTCAR_path = dialog_vasp_band.lineEdit.text()
            self.elements = dialog_vasp_band.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_band.lineEdit_3.text()
            self.vasp_order = dialog_vasp_band.lineEdit_4.text()
            self.np_wannier = dialog_vasp_band.lineEdit_5.text()
            # judge relax
            if dialog_vasp_band.checkBox.checkState() == 2:
                print("Structral relax is turned on!")
            else:
                print("Structral relax is turned off!")
            dialog_vasp_band.close()
            self.output.append("Sent vasp_band task")
            QApplication.processEvents()

        dialog_vasp_band.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_band.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_band.pushButton_2.clicked.connect(self.band_calculation)
        dialog_vasp_band.exec_()

    def vasp_scf_noncal(self):

        dialog_vasp_scf_noncal = Vasp_table_scf_noncal()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_scf_noncal.show()

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR = dialog_vasp_scf_noncal.textEdit.toPlainText()
            self.rel_KPOINTS = dialog_vasp_scf_noncal.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = dialog_vasp_scf_noncal.textEdit_13.toPlainText()
            self.scf_KPOINTS = dialog_vasp_scf_noncal.textEdit_14.toPlainText()
            #
            self.POTCAR_path = dialog_vasp_scf_noncal.lineEdit.text()
            self.elements = dialog_vasp_scf_noncal.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_scf_noncal.lineEdit_3.text()
            self.vasp_order = dialog_vasp_scf_noncal.lineEdit_4.text()
            self.np_wannier = dialog_vasp_scf_noncal.lineEdit_5.text()
            # judge relax
            if dialog_vasp_scf_noncal.checkBox.checkState() == 2:
                print("结构优化")
                self.scf_relax = True
            else:
                print("不需要结构优化")
            # run function
            pass
            dialog_vasp_scf_noncal.close()
            self.output.append("Sent vasp_scf_noncal task")
            QApplication.processEvents()

        dialog_vasp_scf_noncal.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_scf_noncal.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_scf_noncal.pushButton_2.clicked.connect(self.scf_calculation)
        dialog_vasp_scf_noncal.exec_()

    def vasp_band_noncal(self):
        print("vasp_band_noncal")
        dialog_vasp_band_noncal = Vasp_table_band_noncal()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_band_noncal.show()

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR = dialog_vasp_band_noncal.textEdit.toPlainText()
            self.rel_KPOINTS = dialog_vasp_band_noncal.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = dialog_vasp_band_noncal.textEdit_13.toPlainText()
            self.scf_KPOINTS = dialog_vasp_band_noncal.textEdit_14.toPlainText()
            # band
            self.band_INCAR = dialog_vasp_band_noncal.textEdit_19.toPlainText()
            self.band_KPOINTS = dialog_vasp_band_noncal.textEdit_20.toPlainText()
            #
            self.POTCAR_path = dialog_vasp_band_noncal.lineEdit.text()
            self.elements = dialog_vasp_band_noncal.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_band_noncal.lineEdit_3.text()
            self.vasp_order = dialog_vasp_band_noncal.lineEdit_4.text()
            self.np_wannier = dialog_vasp_band_noncal.lineEdit_5.text()
            # judge relax
            if dialog_vasp_band_noncal.checkBox.checkState() == 2:
                print("结构优化")
            else:
                print("不需要结构优化")
            # run function
            pass
            dialog_vasp_band_noncal.close()
            self.output.append("Sent vasp_band_noncal task")
            QApplication.processEvents()

        dialog_vasp_band_noncal.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_band_noncal.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_band_noncal.pushButton_2.clicked.connect(self.band_calculation)
        dialog_vasp_band_noncal.exec_()

    def dos_calculation(self):
        if not self.tran_cal_vasp:
            self.transport_cal_vasp()
        # Change current working directory to self.local_path
        os.chdir(self.local_path)
        # Writing VASP files and transport files

        # scf
        self.write_file_vasp('INCAR_dos', self.scf_INCAR)
        self.transport_file('INCAR_dos')
        self.write_file_vasp('KPOINTS_dos', self.scf_KPOINTS)
        self.transport_file('KPOINTS_dos')

        order1 = 'cd ' + self.node_path + '; '
        order2 = "python cal_vasp_single.py "
        order_npr = 'npr=' + self.np_wannier + ' '
        order_vasp = 'vasp=' + self.vasp_order + ' '
        order_psdir = 'psdir=' + self.POTCAR_path + ' '
        order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
        order_caldir = "cal_dir=" + self.cal_path_name + ' '
        order3 = 'dos=1 '
        order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
        self.output.append("The calculation is started")
        QApplication.processEvents()
        self.remote_session.run_cmd(order_all)
        self.output.append("The calculation is ended")
        QApplication.processEvents()

        if not os.path.exists(os.path.join(self.local_path, "dos")):
            os.mkdir(os.path.join(self.local_path, "dos"))
        eigfile = self.node_path + '/' + self.cal_path_name + '/dos/DOSCAR'
        win = self.local_path + '\\dos\\' + 'DOSCAR'
        print(eigfile, win)
        self.remote_session.get(remote_path=eigfile, local_path=win)
        self.output.append("Task completed, vasp_band file returned")
        QApplication.processEvents()

    def vasp_DOS(self):

        print("vasp_DOS")
        dialog_vasp_DOS = Vasp_table_DOS()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_DOS.show()

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR = dialog_vasp_DOS.textEdit.toPlainText()
            self.rel_KPOINTS = dialog_vasp_DOS.textEdit_2.toPlainText()
            # scf
            self.scf_INCAR = dialog_vasp_DOS.textEdit_13.toPlainText()
            self.scf_KPOINTS = dialog_vasp_DOS.textEdit_14.toPlainText()
            # band
            self.band_INCAR = dialog_vasp_DOS.textEdit_19.toPlainText()
            self.band_KPOINTS = dialog_vasp_DOS.textEdit_20.toPlainText()

            self.POTCAR_path = dialog_vasp_DOS.lineEdit.text()
            self.elements = dialog_vasp_DOS.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_DOS.lineEdit_3.text()
            self.vasp_order = dialog_vasp_DOS.lineEdit_4.text()
            self.np_wannier = dialog_vasp_DOS.lineEdit_5.text()
            # judge relax
            if dialog_vasp_DOS.checkBox.checkState() == 2:
                print("结构优化")
            else:
                print("不需要结构优化")
            # run function
            pass
            dialog_vasp_DOS.close()
            self.output.append("Sent vasp_DOS task")
            QApplication.processEvents()

        dialog_vasp_DOS.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_DOS.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_DOS.pushButton_2.clicked.connect(self.dos_calculation)
        dialog_vasp_DOS.exec_()

    def phonon_calculation(self):
        if not self.tran_cal_vasp:
            self.transport_cal_vasp()
        # Change current working directory to self.local_path
        os.chdir(self.local_path)
        # Writing VASP files and transport files
        self.write_file_vasp('INCAR_phonon_relax', self.rel_INCAR_relax)
        self.transport_file('INCAR_phonon_relax')
        self.write_file_vasp('KPOINTS_phonon_relax', self.rel_KPOINTS_relax)
        self.transport_file('KPOINTS_phonon_relax')

        # phonon
        self.write_file_vasp('INCAR_phonon', self.rel_INCAR_phonon)
        self.transport_file('INCAR_phonon')
        self.write_file_vasp('KPOINTS_phonon', self.rel_KPOINTS_phonon)
        self.transport_file('KPOINTS_phonon')

        order1 = 'cd ' + self.node_path + '; '
        order2 = "python cal_vasp_single.py "
        order_npr = 'npr=' + self.np_wannier + ' '
        order_vasp = 'vasp=' + self.vasp_order + ' '
        order_psdir = 'psdir=' + self.POTCAR_path + ' '
        order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
        order_caldir = "cal_dir=" + self.cal_path_name + ' '
        order3 = 'phonon=1'
        order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
        self.output.append("The calculation is started")
        QApplication.processEvents()
        self.remote_session.run_cmd(order_all)
        self.output.append("The calculation is ended")
        QApplication.processEvents()

        if not os.path.exists(os.path.join(self.local_path, "phonon")):
            os.mkdir(os.path.join(self.local_path, "phonon"))
        eigfile = self.node_path + '/' + self.cal_path_name + '/phonon/band.dat'
        win = self.local_path + '\\phonon\\' + 'band.dat'

        self.remote_session.get(remote_path=eigfile, local_path=win)

        eigfile = self.node_path + '/phonon/band.pdf'
        win = self.local_path + '\\phonon\\' + 'band.pdf'

        self.remote_session.get(remote_path=eigfile, local_path=win)

        self.output.append("Task completed, vasp_phonon file returned")
        QApplication.processEvents()

    def vasp_phonon(self):

        print("vasp_phonon")
        dialog_vasp_phonon = Vasp_table_phonon()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_phonon.show()

        # get parameter
        def vaspfunc_parameter():
            # relax
            self.rel_INCAR_relax = dialog_vasp_phonon.textEdit.toPlainText()
            self.rel_KPOINTS_relax = dialog_vasp_phonon.textEdit_2.toPlainText()
            # phonon
            self.rel_INCAR_phonon = dialog_vasp_phonon.textEdit_3.toPlainText()
            self.rel_KPOINTS_phonon = dialog_vasp_phonon.textEdit_4.toPlainText()

            self.POTCAR_path = dialog_vasp_phonon.lineEdit.text()
            self.elements = dialog_vasp_phonon.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_phonon.lineEdit_3.text()
            self.vasp_order = dialog_vasp_phonon.lineEdit_4.text()
            self.np_wannier = dialog_vasp_phonon.lineEdit_5.text()
            # judge relax
            if dialog_vasp_phonon.checkBox.checkState() == 2:
                print("结构优化")
            else:
                print("不需要结构优化")
            # run function
            pass
            dialog_vasp_phonon.close()
            self.output.append("Sent vasp_phonon task")
            QApplication.processEvents()

        dialog_vasp_phonon.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_phonon.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_phonon.pushButton_2.clicked.connect(self.phonon_calculation)
        dialog_vasp_phonon.exec_()

    def wannier_calculation(self):
        if not self.tran_cal_vasp:
            self.transport_cal_vasp()
        # Change current working directory to self.local_path
        os.chdir(self.local_path)

        # scf
        self.write_file_vasp('INCAR_wan', self.scf_INCAR)
        self.transport_file('INCAR_wan')
        self.write_file_vasp('KPOINTS_wan', self.scf_KPOINTS)
        self.transport_file('KPOINTS_wan')
        # band
        self.write_file_vasp('wannier90.win', self.wannier90_win)
        self.transport_file('wannier90.win')

        order1 = 'cd ' + self.node_path + '; '
        order2 = "python cal_vasp_single.py "
        order_npr = 'npr=' + self.np_wannier + ' '
        order_vasp = 'vasp=' + self.vasp_order + ' '
        order_psdir = 'psdir=' + self.POTCAR_path + ' '
        order_listps = "listps=" + "\'" + self.elements + "\'" + ' '
        order_caldir = "cal_dir=" + self.cal_path_name + ' '
        order3 = 'wan=1 wan_type=normal '
        order_all = order1 + order2 + order_npr + order_vasp + order_psdir + order_listps + order_caldir + order3
        self.output.append("The calculation is started")
        QApplication.processEvents()
        self.remote_session.run_cmd(order_all)
        self.output.append("The calculation is ended")
        QApplication.processEvents()

        if not os.path.exists(os.path.join(self.local_path, "wan")):
            os.mkdir(os.path.join(self.local_path, "wan"))
        eigfile = self.node_path + '/' + self.cal_path_name + '/wan/wannier90_band.dat'
        win = self.local_path + '\\wan\\' + 'wannier90_band.dat'
        print(eigfile, win)
        self.remote_session.get(remote_path=eigfile, local_path=win)
        self.output.append("Task completed, vasp_wan file returned")
        QApplication.processEvents()

    def vasp_wannier(self):
        print("vasp_wannier")
        dialog_vasp_wannier = Vasp_table_wannier()
        # dialog.setModal(True)  # Set modal window
        dialog_vasp_wannier.show()

        # get parameter
        def vaspfunc_parameter():
            self.INCAR = dialog_vasp_wannier.textEdit.toPlainText()
            self.KPOINTS = dialog_vasp_wannier.textEdit_2.toPlainText()
            self.wannier90_win = dialog_vasp_wannier.textEdit_3.toPlainText()
            #
            self.POTCAR_path = dialog_vasp_wannier.lineEdit.text()
            self.elements = dialog_vasp_wannier.lineEdit_2.text()
            self.cal_path_name = dialog_vasp_wannier.lineEdit_3.text()
            self.vasp_order = dialog_vasp_wannier.lineEdit_4.text()
            self.np_wannier = dialog_vasp_wannier.lineEdit_5.text()
            # run function
            pass
            dialog_vasp_wannier.close()
            self.output.append("Sent vasp_wannier task")
            QApplication.processEvents()

        dialog_vasp_wannier.pushButton_2.clicked.connect(vaspfunc_parameter)
        dialog_vasp_wannier.pushButton_2.clicked.connect(self.transport_pos)
        dialog_vasp_wannier.pushButton_2.clicked.connect(self.wannier_calculation)
        dialog_vasp_wannier.exec_()
