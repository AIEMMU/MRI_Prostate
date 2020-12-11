from PyQt5 import QtGui


from typing import *
import numpy as np

def listify(o):
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, str): return [o]
    if isinstance(o, Iterable): return list(o)
    return [o]

def setify(o): return o if instance(o,set) else set(listify(0))

def getPixmap(frame):
    if frame is None: return
    frame = np.array(frame).astype(np.uint8)
    if len(frame.shape) <3:
        frame = np.stack([frame]*3, axis=-1)
    h, w,c = frame.shape
    qImg = QtGui.QImage(frame, w, h,QtGui.QImage.Format_RGB888)
    pixmap = QtGui.QPixmap(qImg)
    return pixmap

def enableButtons(btns, enable):
    for btn in listify(btns):
        btn.setEnabled(enable)

def saveContour(fn, pts):
    np.savetxt(fn,pts)

def loadContour(fn):
    return np.loadtxt(fn)