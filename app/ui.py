# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


# from displayView import MainWindow
#

# from viewer import Viewer
#
# import cv2
import torchvision
def script_method(fn, _rcb=None):
    return fn
def script(obj, optimize=True, _frames_up=0, _rcb=None):
    return obj
import torch.jit
torch.jit.script_method = script_method
torch.jit.script = script

from PyQt5 import QtWidgets, QtGui, QtCore
from displayView import MainWindow
from displayViewModel import *
from dicom import dicom
from predictor import predictor
from utils import getPixmap, enableButtons

def get_y(self): pass

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(DisplayViewModel(enableButtons, getPixmap, dicom(), predictor()))
    window.setGeometry(500, 300, 800, 600)
    window.show()
    window.setWindowTitle('Prostate Segmentor')
    screenGeometry = QtWidgets.QApplication.desktop().screenGeometry()
    x = screenGeometry.width()
    y = screenGeometry.height()
    window.setGeometry(QtCore.QRect(x / 10, y / 10, x / 1.2, y / 1.2))
    sys.exit(app.exec_())