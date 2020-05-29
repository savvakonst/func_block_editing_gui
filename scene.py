

from PySide2 import  QtWidgets as QtGui
from PySide2 import  QtCore ,QtWidgets
from SceneItemPrototype import *
from ScenePrototype import ScenePrototype,MODE









class Scene(ScenePrototype):
    SCENE_IDLE_STATE   = 0
    DRAWING_LINE_STATE = 1
    EDITING_LINE_STATE = 2

    def __init__( self, parent = None ):
        ScenePrototype.__init__(self, parent )
        self.confBackground()

        self.mode  = MODE.ARROW_MODE
        self.state = self.SCENE_IDLE_STATE
        self.nodes=set()


    def mouseMoveEvent(self, event):
        ScenePrototype.mouseMoveEvent(self, event)
        pos = self.roundPos(event)
        if  self.mode == MODE.LINE_MODE and self.state == self.DRAWING_LINE_STATE:
            self.drawVirtualLine(pos)

    def mousePressEvent(self, event):
        ScenePrototype.mousePressEvent(self,event)
        pos = self.roundPos(event)
        if self.mode == MODE.ARROW_MODE:
            self.setMovableLines(True)
            pass
        elif self.mode == MODE.LINE_MODE :
            self.state=self.DRAWING_LINE_STATE ;dbg("DRAWING_LINE_STATE")
            self.addVirtualPath(pos)
        elif self.mode == MODE.ELEMENT_MODE :
            pass

    def mouseReleaseEvent(self, event):
        ScenePrototype.mouseReleaseEvent(self,event)
        pos = self.roundPos(event)

        if  self.state==self.DRAWING_LINE_STATE :
            self.state = self.SCENE_IDLE_STATE ;dbg("SCENE_IDLE_STATE")
            self.refactoring()

        if self.mode == MODE.ARROW_MODE:
            pass
        elif self.mode == MODE.LINE_MODE :
            pass
        elif self.mode == MODE.ELEMENT_MODE :
            pass

    def preRefactoring(self):
        for a in filter(lambda x: x.type() == LINE_t, self.items()):
            if a.line().isNull():
                self.removeItem(a)

        lines=[i for i in filter(lambda x: x.type() == LINE_t, self.items() )]
        linesToRemove=[]
        linesToAdd  = []
        res=False
        linesLen=len(lines)
        print ("linesLen" ,linesLen)
        for j in (linesLen-1-i for i in range(linesLen) ):
            a = lines[j]
            if a.line().isNull():
                self.removeItem(a)
            else :
                for b in lines[0:j]:
                    cmp=b.compare(a)
                    res = cmp.type != CmpRes.NONE
                    if res :
                        linesToAdd+=cmp.newLines
                        linesToRemove+=cmp.oldLines
                        break
                if res :
                    break


        linesToRemove=set(linesToRemove)
        #print linesToRemove
        for i in linesToRemove:
            i.update()
            #print i
            self.removeItem(i)

        for i in linesToAdd:
            self.addItem(i)
            i.updatePositionalParams()

        return res

    def refactoring(self):
        print( "-" * 100 + "start")
        for i in filter(lambda x: x.type() == NODE_t, self.items()) :
            self.removeItem(i)
        print( "-" * 100 + "nodesDeleted")
        while self.preRefactoring():
            pass

        for i in list(self.nodes):
            if  Node.UNION==i.type_:
                i.reduseLines()

        for i in self.nodes:
            self.addItem(i)
            i.printType()

        print( "-" * 100 + "end")






    def removeAllLines(self):
        print( "-" * 100 + "start")
        #lines = filter(lambda x: (x.type() == LINE_t) or (x.type() == NODE_t) , self.items())
        lines = filter(lambda x: (x.type() == NODE_t), self.items())
        for a in lines:
            self.removeItem(a)
        lines = filter(lambda x: (x.type() == LINE_t), self.items())
        for a in lines:
            print( "line " , a.line())
        print( "-" * 100 + "end")

    def removeNullLines(self):
        lines = filter(lambda x: x.type() == LINE_t, self.items())
        for a in lines:
            if a.line().isNull():
                self.removeItem(a)

    def setMovableLines(self,bool):
        lines = filter(lambda x: x.type() == LINE_t, self.items())
        for a in lines:
            a.movable=bool

    def printAllLines(self):
        print( "-" * 32)
        for a in filter(lambda x: x.type() == LINE_t, self.items()):
            print( a.line())
        print( "-" * 32)


    def keyPressEvent(self, QKeyEvent):
        key=QKeyEvent.key()
        self.setMovableLines(False)
        if key == 49:
            self.setMovableLines(True)
            self.mode = MODE.ARROW_MODE ;
        elif key == 50:
            self.mode = MODE.LINE_MODE ;
        elif key == 51:
            self.mode = MODE.ELEMENT_MODE ;
        elif key == 52:
            self.refactoring()
        elif key == 53:
            self.removeAllLines()
        elif key == 54:
            self.removeNullLines()
        if key == 49+9:
            self.printAllLines()


    def moveLine(self):
        pass


    def setVirtualLine(self):
        set

    def drawVirtualLine(self, endPos):
        startPos, middlePos, endPos= self.calcMiddlePos( self.startPos, endPos)
        self.firstVirtualline.setPoints(startPos, middlePos)
        self.secondVirtualline.setPoints(middlePos, endPos)


    def addVirtualPath(self,startPos,*args):
        startPos, middlePos, endPos=self.calcMiddlePos( startPos, *args)
        self.startPos=startPos

        self.firstVirtualline = SceneLinePrototype(LineF(startPos, middlePos))
        self.secondVirtualline = SceneLinePrototype(LineF(middlePos, endPos))

        self.addItem(self.firstVirtualline )
        self.addItem(self.secondVirtualline )









class MyFrame(QtGui.QGraphicsView):



    def __init__( self, parent = None ):
        super( MyFrame, self ).__init__( parent )
        self.setResizeAnchor (QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff);


        self.scene_ = Scene()
        self.setScene( self.scene_ )
        self.resize( 400, 240 )


        x,xi=20,0
        y,yi=20,0
        h=50
        item1 = SceneItemPrototype(x + xi * 30, y + yi * 30, h, h)
        item2 = SceneItemPrototype(x + xi * 30, y + yi * 30, h, h)

        self.scene_.addItem(item1)
        self.scene_.addItem(item2)

        self.setRenderHint(QtExt.QPainter.Antialiasing)


    def wheelEvent(self, event):
        scale_val=1.1 if event.delta()>0 else 0.91
        self.scale(scale_val, scale_val)






if ( __name__ == '__main__' ):
    app = QtGui.QApplication( [] )
    f = MyFrame()
    f.show()
    app.exec_()