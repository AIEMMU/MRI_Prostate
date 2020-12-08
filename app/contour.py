from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPainterPath, QPainterPath, QPainter, QPolygonF, QPen
from PyQt5.QtWidgets import QGraphicsItem

import numpy as np
from scipy import interpolate

class Contour(QtWidgets.QGraphicsItem):

    def __init__(self, line_color = QtGui.QColor(0, 6, 255),
    select_line_color = QtGui.QColor(255, 255, 255),
    vertex_fill_color = QtGui.QColor(0, 255, 0, 255),
    hvertex_fill_color = QtGui.QColor(255, 0, 0),
    point_size = 1.5,
    hsize = 3.0, parent=None):

        super(Contour, self).__init__(parent)
        self.line_color = line_color
        self.select_line_color = select_line_color
        self.vertex_fill_color = vertex_fill_color
        self.hvertex_fill_color = hvertex_fill_color
        self.point_size=point_size
        self.hsize = hsize
        self.selected = False
        self.points = []
        self.hIndex = None
        self.closed = False
        self.adjustPoints = None
        self.objType = None
        self.label = None
        self.editable = False

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def addPoint(self, point):
        self.setSelected(True)
        if self.points and point ==self.points[0]:
            self.closed=True
        else:
            self.points.append(point)
    def popPoint(self):
        if self.points:
            return self.points.pop()
        return None
    def size(self):
        return len(self.points)


    def paint(self, painter, option, widget):
        if self.points:
            self.prepareGeometryChange()
            color =  self.line_color
            pen = QPen(color)
            pen.setWidth(self.point_size / 2)
            painter.setPen(pen)
            path = self.shape()
            if self.closed == True:
                path.closeSubpath()
            painter.drawPath(path)
            vertex_path = QPainterPath()
            self.drawVertex(vertex_path, 0)
            [self.drawVertex(vertex_path, i) for i in range(len(self.points))]
            painter.drawPath(vertex_path)
            painter.fillPath(vertex_path, self.line_color)

    def drawVertex(self, path, idx):
        psize = self.point_size
        if idx == self.hIndex:
            psize = self.hsize
            if self.hIndex is None:
                self.vertex_fill_color = self.hvertex_fill_color
        else:
            self.vertex_fill_color = QtGui.QColor(0, 255, 0, 255)
        path.addEllipse(self.mapFromScene(self.points[idx]), psize, psize)

    def shape(self):
        path = QPainterPath()
        poly = self.mapFromScene(QtGui.QPolygonF(self.points))
        path.addPolygon(poly)
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

    def moveBy(self, tomove, delta):
        if tomove == 'all':
            tomove = slice(0, len(self.points))
        else:
            tomove = slice(tomove, tomove + 1)
        self.points[tomove] = [point + delta for point in self.points[tomove]]

    def highlightVertex(self, index):
        self.hIndex = index

    def highlightClear(self):
        self.hIndex = None
        self.selected = False

    def remove(self, idx):
        del self.points[idx]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __getitem__(self, item):
        return self.points[item]

    def __len__(self):
        return len(self.points)
