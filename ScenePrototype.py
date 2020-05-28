from PySide2 import  QtGui as QtExt
from PySide2 import  QtWidgets as QtGui
from PySide2 import  QtCore ,QtWidgets
from common import *



class ScenePrototype(QtGui.QGraphicsScene):
    GRID_SIZE = 10


    def __init__(self,parent = None ):
        self.backgroundEnable=False
        QtGui.QGraphicsScene.__init__(self, parent)

    def confBackground(self ,Nx=100 ,Ny=50 ,backgroundPen=QtExt.QPen(BLACK_COLOR ,0)):
        self.backgroundPen =backgroundPen
        self.poly=QtExt.QPolygon()
        for i in range(-Nx ,Nx):
            for j in range(-Ny ,Ny):
                self.poly.append(QtCore.QPoint( i * self.GRID_SIZE, j * self.GRID_SIZE))
        self.backgroundEnable = True


    def drawBackground(self, painter, rect):
        if self.backgroundEnable :
            painter.setPen(self.backgroundPen)
            painter.drawPoints(self.poly)

    def calcMiddlePos(self,startPos,*args):
        le=len(args)
        if le == 0:
            endPos = startPos
            middlePos = startPos
        elif le == 1:
            endPos=args[0]
            vector=(endPos-startPos)
            x,y = (startPos.x(),endPos.y()) if abs(vector.x())< abs(vector.y()) else (endPos.x(),startPos.y())
            middlePos = QtCore.QPoint(x,y)
        elif le == 2:
            endPos = args[1]
            middlePos = args[0]

        return  startPos, middlePos, endPos

    def roundPos(self,event):
        return (event.scenePos() / self.GRID_SIZE ).toPoint() * self.GRID_SIZE

    def removeItem(self, item):
        if (item.type() == LINE_t) or (item.type() == NODE_t):

            item.preRemove()
        QtGui.QGraphicsScene.removeItem(self, item)