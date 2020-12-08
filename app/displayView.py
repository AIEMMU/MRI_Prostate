from PyQt5 import QtWidgets, uic, QtCore, QtGui
from viewer import Viewer

from contour import Contour
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,model):
        self.model = model
        super(MainWindow, self).__init__() #call the inherited class __init__ method
        uic.loadUi("gui.ui", self) # load teh UI file

        self.dicomViewer = self.findChild(Viewer, 'dicomViewer')
        self.dicomViewer.setAlignment(QtCore.Qt.AlignCenter)

        # self.dicomViewer.dicom_clicked.connect(self.clicked)
        # # Buttons!
        self.genButton = self.findChild(QtWidgets.QPushButton, 'genButton')
        self.genButton.clicked.connect(self.gen)  # remeber to pass the definition of the method

        self.editButton = self.findChild(QtWidgets.QPushButton, 'editButton')
        self.editButton.clicked.connect(self.editContour)

        self.resetButton = self.findChild(QtWidgets.QPushButton, 'resetButton')
        self.resetButton.clicked.connect(self.reset)  # remeber to pass the definition of the method

        self.contourButton = self.findChild(QtWidgets.QPushButton, 'contourButton')
        self.contourButton.clicked.connect(self.drawContour)  # remeber to pass the definition of the method

        self.navButton = self.findChild(QtWidgets.QPushButton, 'navButton')
        self.navButton.clicked.connect(self.navContour)  # remeber to pass the definition of the method
        #menu button
        self.LoadDicom = self.findChild(QtWidgets.QAction, 'loadDicom')
        self.LoadDicom.triggered.connect(self.load)

        self.saveContour = self.findChild(QtWidgets.QAction, 'saveContour')
        self.saveContour.triggered.connect(self.SaveContour)

        self.loadContour = self.findChild(QtWidgets.QAction, 'loadContour')
        self.loadContour.triggered.connect(self.LoadContour)

    def LoadContour(self):
        pts = self.model.loadContour()
        if pts is None:return
        self.dicomViewer.addContour(pts)

    def SaveContour(self):
        pts = self.dicomViewer.returnPoints()
        if pts is None: return
        self.model.saveContour(pts)

    def load(self):
        self.dicomViewer.reset()
        pixmap = self.model.loadDicom()
        if pixmap is None: return
        self.dicomViewer.setImage(pixmap)

    def editContour(self):
        self.dicomViewer.toggleEdit()

    def drawContour(self):
        self.dicomViewer.toggleDrawing()
    def navContour(self):
        self.dicomViewer.toggleNav()
    def gen(self):
        if self.dicomViewer.hasDicom():
            plane = self.model.get_plane()
            if not plane:
                buttonReply = QMessageBox.question(self, 'PyQt5 message', "This dicom file is not an Axial Slice.\nthis AI network was trained on Axial slices and may not produce good results on non axial slices.\nDo you wish to contine?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply ==QMessageBox.No:
                    return
            contour = self.model.get_contour()
            if contour is None: return
            self.dicomViewer.addContour(contour)

    def reset(self):
        self.dicomViewer.reset()

    # def clicked(self, pos,):

        # if self.dicomViewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:









