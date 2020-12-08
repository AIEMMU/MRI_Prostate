from PyQt5 import QtWidgets
from utils import loadContour, saveContour

class DisplayViewModel():
    def __init__(self, enableButtons, getPixmap, dicom, predictor):
        self.enableButtons, self.getPixmap = enableButtons, getPixmap
        self.dicom = dicom
        self.predictor = predictor

    def updateImage(self, w,l):
        self.img = self.dicom.setWL(w,l)

        return self.update()
    def loadContour(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Contour file", "", "Txt file (*.txt)")
        if not fn:return
        return loadContour(fn)

    def saveContour(self, pts):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save output contour file(*.txt)", "", "Txt Files (*.txt)")
        if fn == '': return
        saveContour(fn, pts)

    def loadDicom(self):
        fn, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Dicom", "", "Dicoms (*.dcm)")
        if not fn: return
        self.img = self.dicom.get_dicom(fn)
        return self.update()

    def update(self):
        return self.getPixmap(self.img)

    def get_plane(self):
        if self.dicom.file_plane() == 'Axial':
            return True
        return False

    def get_contour(self):
        contour = self.predictor.predict(self.dicom.updateImage())
        return contour



