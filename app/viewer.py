from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from contour import Contour

import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    idx = sorted((np.abs(array - value)))
    return array[idx]
def distance(p):
    return p.x()**2 + p.y()**2

class SubScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None, dist = distance, eps=30, modes = [0,1,2]):
        super().__init__(parent)
        self.mode = modes[0]
        self.modes = modes
        self.QGitem=None
        self.line = None
        self.polys = []
        self.dist_func = dist
        self.eps = eps
        self.polyFinished = False
        self.selectedContour = None
        self.selectedVertex=None
        self.overrideCursor(QtCore.Qt.ArrowCursor)

    def setDrawing(self):
        self.mode = self.modes[1]
    def setEdit(self):
        self.mode = self.modes[2]
    def setMovement(self):
        self.mode = self.modes[0]

    def updatePolyPoint(self, poly, pos):
        poly.setPos(pos)
        poly.addPoint(pos)

    def clearContours(self):
        if self.selectedContour:
            self.selectedContour.highlightClear()
            self.selectedContour = None
            self.forceClearContours()
            self.update()

    def forceClearContours(self):
        for contour in self.items()[:-1]:
            contour.highlightClear()
        self.update()

    def returnPoints(self):
        if self.QGitem is not None:
            pts = self.QGitem.points
        elif len(self.polys) > 0:
            pts = self.polys[0].points
        else:
            return None
        return [[p.x(), p.y()] for p in pts]
    def addAIPolygon(self, points):
        qPoints = [QtCore.QPoint(x,y) for x,y in points]#
        if len(self.polys) ==0:
            if self.QGitem is None:
                self.QGitem = Contour(point_size=1.5)
                self.addItem(self.QGitem)
                self.updatePolyPoint(self.QGitem, qPoints[0])
                self.QGitem.setZValue(len(self.polys) + 1)
            self.QGitem.prepareGeometryChange()
            self.QGitem.points = qPoints
            self.QGitem.points.append((qPoints[0]))
        else:
            self.selectedContour = self.polys[0]
            self.selectedContour.prepareGeometryChange()
            self.selectedContour.points = qPoints
            self.selectedContour.points.append((qPoints[0]))
        self.finalisePolygon()
        self.update()

    def mouseReleaseEvent(self, event):
        if self.mode == self.modes[0]:
            self.overrideCursor(QtCore.Qt.ArrowCursor)
            self.update()

    def isClose(self, p1, p2):
        return self.dist_func(p1-p2) <self.eps

    def finalisePolygon(self, premature=False):
        if self.QGitem:
            # if premature: something to do but will add later
            if self.line:
                self.removeItem(self.line)
                self.line.popPoint()
            self.QGitem.editable=False
            self.polys.append(self.QGitem)
            self.QGitem = None
            self.mode = self.modes[0]
        self.update()

    def selectContour(self, contour):
        contour.selected=True
        self.selectedContour = contour
        self.update()

    def selectShapeByPoint(self, pos):
        if self.vertexSelected():
            self.selectedContour.highlightVertex(self.selectedVertex)
            return
        itemundermouse = self.itemAt(pos, QtGui.QTransform())
        if itemundermouse in self.items()[:-1]:
            self.selectContour(itemundermouse)
            return

    def moveVertex(self, pos):
        self.selectedContour.prepareGeometryChange()
        self.selectedContour.moveBy(self.selectedVertex, pos - self.selectedContour[self.selectedVertex])

    def vertexSelected(self):
        return self.selectedVertex is not None

    def ptDist(self, pt1, pt2):
        # A line between both
        line = QtCore.QLineF(pt1, pt2)
        # Length
        lineLength = line.length()
        return lineLength

    def getClosestPoint(self, pt):
        closest = (-1, -1)
        distTh = 4.0
        dist = 1e9  # should be enough
        item_under_mouse = self.itemAt(pt, QtGui.QTransform())
        for i in range(self.selectedContour.size()):
            pt1 = self.selectedContour.points[i]
            j = i+1
            if j == self.selectedContour.size():
                j=0
            pt2 = self.selectedContour.points[j]
            edge = QtCore.QLineF(pt1, pt2)
            normal = edge.normalVector()
            normalTrhoughPos = QtCore.QLineF(pt.x(), pt.y(), pt.x()+normal.dx(), pt.y()+normal.dy())
            if item_under_mouse not in self.items()[:-1]:
                normalTrhoughPos = QtCore.QLineF(pt.x(), pt.y(), pt.x() - normal.dx(), pt.y() - normal.dy())
            intersectionPt = QtCore.QPointF()
            intersectionType = edge.intersect(
                normalTrhoughPos, intersectionPt)

            if intersectionType ==QtCore.QLineF.BoundedIntersection:
                currDist = self.ptDist(intersectionPt, pt)
                if currDist < dist:
                    closest = (i,j)
                    dist = currDist

        return closest

    def reset(self):
        self.clearContours()
        self.forceClearContours()

        if self.line:
            self.removeItem(self.line)
            self.line=None
        if self.QGitem:
            self.removeItem(self.QGitem)
            self.QGitem = None

        for polys in self.polys:
            self.removeItem(polys)
        self.polys = []
        self.mode = self.modes[0]
        self.update()

    def mousePressEvent(self, event):

        pos = event.scenePos()
        if event.button() == QtCore.Qt.LeftButton and self.mode == self.modes[1]:
            self.overrideCursor(QtCore.Qt.CrossCursor)
            if self.line is None or self.polyFinished:
                self.line = Contour(point_size=1.5)
                self.addItem(self.line)
                self.updatePolyPoint(self.line, pos)

            elif self.line and not self.polyFinished:
                self.line.prepareGeometryChange()
                self.line.points[0] = pos
                self.line.setPos(pos)

            if self.QGitem:
                self.QGitem.prepareGeometryChange()
                if len(self.QGitem.points) >1 and self.isClose(pos, self.QGitem.points[0]):
                    self.overrideCursor(QtCore.Qt.PointingHandCursor)
                    pos = self.QGitem.points[0]
                    self.QGitem.highlightVertex(0)
                #need to add to close the polygone
                self.QGitem.addPoint(pos)
                if self.QGitem.points[0] == pos:
                    self.finalisePolygon()
            else:
                self.QGitem = Contour(point_size=1.5)
                self.addItem(self.QGitem)
                self.updatePolyPoint(self.QGitem, pos)
                self.QGitem.setZValue(len(self.polys)+1)
            event.accept()
            self.update()

        if event.button() == QtCore.Qt.RightButton and self.mode == self.modes[1]:
            self.overrideCursor(QtCore.Qt.CrossCursor)
            if self.line:
                if len(self.line.points) > 1 and self.QGitem:
                    self.QGitem.prepareGeometryChange()
                    self.QGitem.remove(-1)
                    if self.QGitem.points==1:
                        self.removeItem(self.QGitem)
                        self.removeItem(self.line)
                        self.line=None
                        return
                    self.line.prepareGeometryChange()
                    self.line.points[0] =self.QGitem.points[-1]
                event.accept()
                self.update()

        if self.mode == self.modes[2] and event.button() == QtCore.Qt.LeftButton:
            self.overrideCursor(QtCore.Qt.ClosedHandCursor)
            self.selectShapeByPoint(pos)

            event.accept()
            self.update()

        if self.mode == self.modes[2] and event.button() == QtCore.Qt.MiddleButton:
            self.overrideCursor(QtCore.Qt.CrossCursor)
            if len(self.polys) > 0:
                self.selectedContour = self.polys[0]
                pts = self.getClosestPoint(pos)
                self.selectedContour.points.insert(pts[1], pos)


        if self.vertexSelected() and event.button() == QtCore.Qt.RightButton and self.mode == self.modes[2]:
            self.overrideCursor(QtCore.Qt.PointingHandCursor)
            self.selectedContour.prepareGeometryChange()
            self.selectedContour.remove(self.selectedVertex)

            if len(self.selectedContour.points) ==1:
                self.removeItem(self.selectedContour)
            self.update()

    def overrideCursor(self, cursor):
        QtWidgets.QApplication.setOverrideCursor(cursor)

    def mouseMoveEvent(self, event):

        pos = event.scenePos()
        if self.mode == self.modes[1]:
            self.overrideCursor(QtCore.Qt.CrossCursor)
            if self.QGitem:
                if len(self.QGitem.points)==1: #intilaise line to the pooint
                    self.line.points = [self.QGitem.points[0],self.QGitem.points[0] ]
                colorLine = QtGui.QColor(3,252,66)

                if len(self.QGitem.points) >1 and self.isClose(pos, self.QGitem.points[0]):
                    self.overrideCursor(QtCore.Qt.PointingHandCursor)
                    colorLine = self.QGitem.line_color
                    pos = self.QGitem[0]
                    self.QGitem.highlightVertex(0)

                if len(self.line.points)==2:
                    self.line.points[1] = pos
                else:
                    self.line.addPoint = pos
                self.line.line_color = colorLine
            return

        if self.mode == self.modes[2] and QtCore.Qt.LeftButton & event.buttons():


            if self.vertexSelected():
                self.overrideCursor(QtCore.Qt.ClosedHandCursor)
                self.selectedContour.prepareGeometryChange()
                self.moveVertex(pos)
                self.update()

        elif self.mode == self.modes[2]:
            self.overrideCursor(QtCore.Qt.OpenHandCursor)

        id_point = [[i for i, y in enumerate(poly.points) if distance(pos - y) <= self.eps] for poly in self.polys]
        id_shape = [i for i, y in enumerate(id_point) if y != []]

        item_under_mouse = self.itemAt(pos, QtGui.QTransform())
        self.clearContours()
        if id_shape!=[]:
            self.selectedVertex = id_point[id_shape[0]][0]
            self.selectContour(self.items()[:-1][::-1][id_shape[0]])
            self.selectedContour.highlightVertex(self.selectedVertex)
        elif item_under_mouse in self.items()[:-1]:
            self.selectedVertex=None
            self.selectContour(item_under_mouse)
            self.selectedContour.hIndex=None

        else:
            self.selectedVertex = None
        self.update()

class Viewer(QtWidgets.QGraphicsView):
    dicom_clicked = QtCore.pyqtSignal(QtCore.QPoint)
    dicom_move = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(Viewer, self).__init__(parent)
        self.zoom = 0
        self.dicom = True
        self.dicom_image = QtWidgets.QGraphicsPixmapItem()
        self.dicom_image.setZValue(-1)
        self._scene = SubScene(self)
        self._scene.addItem(self.dicom_image)

        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setScene(self._scene)
    def addContour(self, contour):
        self._scene.addAIPolygon(contour)

    def hasDicom(self):
        return not self.dicom

    def toggleDrawing(self):
        self._scene.setDrawing()
    def toggleEdit(self):
        self._scene.setEdit()
    def toggleNav(self):
        self._scene.setMovement()

    def fitInView(self, scale = True):
        rect = QtCore.QRectF(self.dicom_image.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.dicom_image:
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)

    def wheelEvent(self, event):
        if self.hasDicom():
            if event.angleDelta().y() > 0:
                factor = 1.15
                self.zoom +=1
            else:
                factor = 0.8
                self.zoom -= 1
            if self.zoom>0:
                self.scale(factor, factor)
            elif self.zoom ==0:
                self.fitInView()
            else:
                self.zoom=0

    def add_item(self, item):
        self._scene.addItem(item)

    def changeImage(self, img=None):
        if img and not img.isNull():
            self.dicom_image.setPixmap(img)

    def setImage(self, img=None):
        self.zoom = 0
        if img and not img.isNull():
            self.dicom = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.dicom_image.setPixmap(img)
        else:
            self.dicom = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self.dicom_image.setPixmap(QtGui.QPixmap())
        self.fitInView()
    def returnPoints(self):
        return self._scene.returnPoints()
    def reset(self):
        self._scene.reset()
        self.fitInView()

    def toggleStates(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)



