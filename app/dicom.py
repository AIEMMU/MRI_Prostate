
import pydicom
from fastai.vision.all import *
from fastai.medical.imaging import *

class dicom():

    def get_dicom(self, fn):
        f = pydicom.dcmread(fn)
        self._iop =f.ImageOrientationPatient
        self._dicom_array = tensor(f.pixel_array)
        self._w, self._l = self._dicom_array.max(), self._dicom_array.min()
        return self.updateImage()

    def setWL(self, w,l):
        self._w, self._l = w,l
        return self.updateImage()
    def getShape(self):
        return self.dicom_array.shape()

    def updateImage(self,):
        img = self._dicom_array.clone()
        img = img.windowed(self._w, self._l)
        brks = img.freqhist_bins(n_bins=3500)
        img = PILImage.create(img.hist_scaled(brks) * 255)
        return img

    def file_plane(self): #will need to check this code works with Cheng
        IOP_round = [round(x) for x in self._iop]
        plane = np.cross(IOP_round[0:3], IOP_round[3:6])
        plane = [abs(x) for x in plane]
        if plane[0] == 1:
            return "Sagittal"
        elif plane[1] == 1:
            return "Coronal"
        elif plane[2] == 1:
            return "Axial"
