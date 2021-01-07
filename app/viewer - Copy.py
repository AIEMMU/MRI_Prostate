import cv2
import torch
import torchvision
def script_method(fn, _rcb=None):
    return fn
def script(obj, optimize=True, _frames_up=0, _rcb=None):
    return obj
import torch.jit
torch.jit.script_method = script_method
torch.jit.script = script
import fastai.losses
import fastai.layers

fastai.layers.BaseLoss = fastai.losses.BaseLoss
fastai.layers.CrossEntropyLossFlat = fastai.losses.CrossEntropyLossFlat
fastai.layers.BCEWithLogitsLossFlat = fastai.losses.BCEWithLogitsLossFlat
fastai.layers.BCELossFlat = fastai.losses.BCELossFlat
fastai.layers.MSELossFlat = fastai.losses.MSELossFlat
fastai.layers.L1LossFlat = fastai.losses.L1LossFlat
fastai.layers.LabelSmoothingCrossEntropy = fastai.losses.LabelSmoothingCrossEntropy
fastai.layers.LabelSmoothingCrossEntropyFlat = fastai.losses.LabelSmoothingCrossEntropyFlat

import skimage
import pydicom
import PyQt5
from fastai.vision.all import *
import fastcore
print('hello')