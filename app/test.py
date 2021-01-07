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
import torch

a = torch.tensor((1,2))
print(a)