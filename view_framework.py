

from PySide2 import  QtGui as QtExt
from PySide2 import  QtWidgets as QtGui
from PySide2 import  QtCore ,QtWidgets
from scene_framework import  Point ,Scene


BLACK_COLOR=QtCore.Qt.black
RED_COLOR=QtExt.QColor("#ff0000")
GREEN_COLOR=QtExt.QColor("#008f00")
VIOLET_COLOR= QtExt.QColor("#7d0779")
BLUE_COLOR= QtExt.QColor("#0000eb")


class SceneFW(Scene):
    def __init__(self,frontEndScene):
        self.frontEndScene=frontEndScene

    def plot(self):
        for i in self.lineList :
            pass
            #self.frontEndScene


class ScenePrototype(QtGui.QGraphicsScene):
    GRID_SIZE = 10

    def __init__(self,parent = None ):
        self.backgroundEnable=False
        QtGui.QGraphicsScene.__init__(self, parent)
        self.confBackground()

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


    def roundPos(self,event):
        p=(event.scenePos() / self.GRID_SIZE)
        p=Point(p.x(),p.y())* self.GRID_SIZE
        return p

    def keyPressEvent(self, event: QtExt.QKeyEvent):
        print( event)

    def mousePressEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        pos = self.roundPos(event)
        pass

    def mouseReleaseEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        pos = self.roundPos(event)
        pass

    def mouseMoveEvent(self, event:QtWidgets.QGraphicsSceneMouseEvent):
        pos = self.roundPos(event)
        pass




class MyFrame(QtGui.QGraphicsView):




    def __init__( self, parent = None ):
        super( MyFrame, self ).__init__( parent )
        self.setResizeAnchor (QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);


        scene = ScenePrototype()
        self.setScene( scene )
        self.resize( 400, 240 )

        pencil = QtExt.QPen( QtCore.Qt.black, 2)
        pencil.setStyle( QtCore.Qt.SolidLine )


        polygon = QtExt.QPolygonF([QtCore.QPointF(250, 100), QtCore.QPointF(400, 250), QtCore.QPointF(200, 150)])

        brush = QtExt.QBrush( QtExt.QColor( 125, 125, 125, 125 ) )
        scene.addPolygon( polygon, pencil, brush )

        self.xr=400

        self.setRenderHint(QtExt.QPainter.Antialiasing)


    def plot2(self):
        self.xr=-self.xr
        pencil = QtExt.QPen( QtCore.Qt.black, 2)
        pencil.setStyle( QtCore.Qt.SolidLine )

        polygon = QtExt.QPolygonF([QtCore.QPointF(self.xr+250, 100), QtCore.QPointF(self.xr+400, 250), QtCore.QPointF(self.xr+200, 150)])

        brush = QtExt.QBrush( QtExt.QColor( 125, 125, 125, 125 ) )
        self.scene().addPolygon( polygon, pencil, brush )

    def wheelEvent(self, event):
        self.plot2()
        scale_val=1.1 if event.delta()>0 else 0.91
        self.scale(scale_val, scale_val)


if ( __name__ == '__main__' ):
    app = QtGui.QApplication( [] )
    f = MyFrame()
    f.show()
    app.exec_()