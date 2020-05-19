from PyQt4 import QtGui, QtCore
from common import *



class LineF(QtCore.QLineF):
    def __init__(self, *args, **kwargs):
        QtCore.QLineF.__init__(self, *args, **kwargs)




class CmpRes():
    NONE=0
    CROSS=1
    CORNER=2
    UNION=3
    MATCH=4

    def __init__(self,type,oldLines=(),newLines=()):
        self.type=type
        self.oldLines=oldLines
        self.newLines=newLines




class Node(QtGui.QGraphicsEllipseItem):
    NONE=0
    CROSS=1
    CORNER=2
    UNION=3
    widthPoint=QtCore.QPoint(2,2)
    mainBrush= QtGui.QBrush(MAIN_LINE_COLOR, QtCore.Qt.SolidPattern)
    subBrush = QtGui.QBrush(SUB_LINE_COLOR,QtCore.Qt.SolidPattern)

    def __init__(self, lines=[],pos=()):
        self.pos=pos
        self.lines=lines
        self.type_=self.NONE
        QtGui.QGraphicsEllipseItem.__init__(self,QtCore.QRectF(pos-self.widthPoint,pos+self.widthPoint))
        self.setBrush(self.mainBrush)

    def addLine(self,line):
        self.lines.append(line)
        if len(self.lines)>4 :
            print "ERROR NODE : len == "+str(len(self.lines))
        self.typeUpdate()

    def getType(self):
        return len(self.lines)

    def typeUpdate(self):
        len_=len(self.lines)
        if len_==2:
            self.type_ = self.UNION if self.lines[0].orientation==self.lines[1].orientation else self.CORNER
            #self.setBrush(self.subBrush)
            self.setVisible(False)
        elif len_>2:
            self.type_ = self.CROSS
            self.setBrush(self.mainBrush)
            self.setVisible(True)
        else:
            self.type_ = self.NONE

    def printType(self):
        if   self.type_ == self.NONE   : print "node type NONE  "
        elif self.type_ == self.CROSS  : print "node type CROSS "
        elif self.type_ == self.CORNER : print "node type CORNER"
        elif self.type_ == self.UNION  : print "node type UNION "

    def removeLine(self,line):
        scene=line.scene()
        self.lines.remove(line)
        if len(self.lines)<1:
            scene.nodes.remove(self)

    def preRemove(self):
        for i in self.lines :
            i.removeNode(self)
        self.lines=[]
        self.scene().nodes.remove(self)

    def getOtherLines(self,line):
        res=[]
        for i in self.lines :
            if line != i :
                res.append(i)
        return res


    def reduseLines(self):
        if self.type_ == self.UNION :
            a,b=self.lines
            self.lines = []

            scene=a.scene()
            new_line=SceneLinePrototype()
            aNode,aPos,aDirection = (a.right.node,a.getRightPos(),True ) if a.left.node == self else (a.left.node,a.getLeftPos(),False)
            bNode,bPos,bDirection = (b.right.node,b.getRightPos(),True ) if b.left.node == self else (b.left.node,b.getLeftPos(),False)

            new_line.preSetPoints(bPos, aPos)


            if aDirection  :
                new_line.preSetPoints(bPos, aPos)
            else :
                new_line.preSetPoints(aPos, bPos)



            if not aNode is None:
                aNode.removeLine(a)
                aNode.addLine(new_line)

            if not bNode is None:
                bNode.removeLine(b)
                bNode.addLine(new_line)

            if aDirection  :
                #new_line.preSetPoints(bPos, aPos)
                new_line.right.setNode(aNode)
                new_line.left.setNode(bNode)
            else :
                #new_line.preSetPoints(aPos, bPos)
                new_line.right.setNode(bNode)
                new_line.left.setNode(aNode)

            a.clear()
            b.clear()

            scene.removeItem(a)
            scene.removeItem(b)
            scene.addItem(new_line)
            scene.nodes.remove(self)











def newLine(l,r,h,orientation):
    line=SceneLinePrototype()
    line.setPositionalParams(l,r,h,orientation)
    return line

def newPoint(s,h,orientation):
    point = QtCore.QPointF(s, h) if orientation == HOEIZONTAL else QtCore.QPointF(h, s)
    return point

def isContain(p,l,r):
    return (l<p and p<r)

def isContact(p,l,r):
    return (l==p) or (p==r)

def setNode(a,b,scene=None):
    if a.getLeftPos() == b.getLeftPos():
        pos=a.getLeftPos()
        aNode,bNode=a.left,b.left
    elif a.getRightPos() == b.getRightPos():
        pos =a.getRightPos()
        aNode,bNode=a.right,b.right
    elif a.getLeftPos() == b.getRightPos():
        pos = a.getLeftPos()
        aNode,bNode=a.left,b.right
    elif a.getRightPos() == b.getLeftPos():
        pos = a.getRightPos()
        aNode,bNode=a.right,b.left
    else:
        return

    if aNode.node is None and bNode.node is None :
        node = Node([a,b], pos)
        aNode.node = node
        bNode.node = node
    elif aNode.node is None :
        aNode.node=bNode.node
        aNode.node.addLine(a)
        node=aNode.node
    elif bNode.node is None:
        bNode.node = aNode.node
        bNode.node.addLine(b)
        node=bNode.node
    else:
        return


    node.typeUpdate()
    if scene is None :
        a.scene().nodes.add(node)
    else :
        scene.nodes.add(node)




class Proto():
    def __init__(self, *args, **kwargs):
        self.setAcceptHoverEvents(True)
        self.state = IDLE_STATE
        self.hover = False
        self.deltaPos=QtCore.QPointF()
        self.children=[]
        self.setPen(QtGui.QPen(BLACK_COLOR, 10, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin))

    def hoverEnterEvent(self, event):
        self.hover = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hover = False
        self.update()

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        pa = menu.addAction('Delete')
        pa = menu.addAction('Parameters')
        menu.exec_(event.screenPos())

    def mousePressEvent(self, event):
        self.deltaPos=event.scenePos()




class SceneLinePrototype(QtGui.QGraphicsLineItem,Proto):

    zeroPoint = QtCore.QPointF(0,0)

    class nodeIfs():
        def __init__(self,parent):
            self.node=None
            self.parent=parent

        def setNode(self,node):
            self.node=node

        def isEmpty(self):
            if (self.node is None) :
                return True
            else :
                return len(self.node.lines)<2

        def isEmpty(self):
            if (self.node is None) :
                return True
            else :
                return len(self.node.lines)<2

        def isCorner(self):
            if (self.node is None) :
                return False
            else :
                return len(self.node.lines)==2


        def eq(self, other):
            return other == self.node

        def clear(self):
            self.node=None

        def remove(self):
            if not (self.node is None):
                self.node.removeLine(self.parent)
            del(self.node)
            del(self.parent)

    def clear(self):
        self.left.clear()
        self.right.clear()


    def __init__(self, *args, **kwargs):
        QtGui.QGraphicsLineItem.__init__(self, *args, **kwargs)
        Proto.__init__(self, *args, **kwargs)
        self.movable=False
        self.setFlags(self.ItemIsSelectable)#| self.ItemIsMovable
        self.orientation=VERTICAL
        self.setPos(0,0)
        self.h,self.l, self.r=0,0,0
        self.onMove = False
        self.left  = self.nodeIfs(self)
        self.right = self.nodeIfs(self)

        self.leftLine = None
        self.rightLine = None

    def getLeftPos(self):
        return self.line().p1()

    def getRightPos(self):
        return self.line().p2()

    def paint(self, painter, option, widget):
        lineStyle,space =  (SUB_LINE_STYLE,5) if self.isSelected() else (MAIN_LINE_STYLE,0)
        color = SUB_LINE_COLOR if self.hover else  MAIN_LINE_COLOR
        pen=QtGui.QPen(color, 0, lineStyle, QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin)
        #pen.setDashPattern([5,space])
        painter.setPen(pen)
        painter.drawLine(self.line())

    def mouseMoveEvent(self, event):
        QtGui.QGraphicsLineItem.mouseMoveEvent(self, event)
        if self.movable:
            pos = ((event.scenePos() - self.deltaPos) / 10).toPoint() * 10
            pos.setX(0) if self.orientation == HOEIZONTAL else pos.setY(0)


            if self.zeroPoint!=pos or self.onMove:
                if not self.onMove:
                    self.scene().state = self.scene().DRAWING_LINE_STATE
                    if not self.left.isEmpty() :
                        if self.left.isCorner():
                            lineToRemove=self.left.node.getOtherLines(self)[0]
                            le,re = lineToRemove.getLeftPos() , lineToRemove.getRightPos()
                            self.lastP1_ =  re  if le == self.lastP1 else le
                            self.scene().removeItem(lineToRemove)
                        self.leftLine = SceneLinePrototype()
                        self.scene().addItem(self.leftLine)

                    if not self.right.isEmpty() :
                        if self.right.isCorner():
                            lineToRemove=self.right.node.getOtherLines(self)[0]
                            le,re=lineToRemove.getLeftPos() , lineToRemove.getRightPos()
                            self.lastP2_ =  re  if le == self.lastP2 else le
                            self.scene().removeItem(lineToRemove)
                        self.rightLine = SceneLinePrototype()
                        self.scene().addItem(self.rightLine)


                self.onMove=True
                p1,p2 =self.lastP1+pos,self.lastP2+pos
                self.setLine(LineF(p1, p2))
                self.update()
                self.updatePositionalParams()

                if not (self.leftLine is None):
                    self.leftLine.setPoints(self.lastP1_,p1)
                if not (self.rightLine is None):
                    self.rightLine.setPoints(self.lastP2_,p2)


    def mousePressEvent(self, event):
        QtGui.QGraphicsLineItem.mousePressEvent(self, event)
        self.deltaPos=( event.scenePos() / 10 ).toPoint() * 10
        self.lastP1,self.lastP2=self.line().p1(),self.line().p2()
        self.lastP1_,self.lastP2_=self.lastP1,self.lastP2

    def mouseReleaseEvent(self, event):
        QtGui.QGraphicsLineItem.mouseReleaseEvent(self, event)
        self.onMove = False
        self.leftLine = None
        self.rightLine = None
        #self.scene().state = self.scene().SCENE_IDLE_STATE

    def updatePositionalParams(self):
        x, y =0.0 ,0.0;
        if self.orientation == HOEIZONTAL:
            self.h = self.line().p1().y()+y
            self.l, self.r = self.line().p1().x()+x, self.line().p2().x()+x
        else:
            self.h = self.line().p1().x()+x
            self.l, self.r = self.line().p1().y()+y, self.line().p2().y()+y

    def setPositionalParams(self,l,r,h,orientation):
        line= LineF(l,h,r,h) if orientation==HOEIZONTAL else LineF(h,l,h,r)
        self.orientation=orientation
        self.setLine(line)
        self.setPos(0,0)
        self.update()

    def setPoints(self, startPos,endPos):
        self.orientation=HOEIZONTAL if startPos.y()==endPos.y() else VERTICAL

        if (startPos.y()>endPos.y()) or (startPos.x()>endPos.x() ):
            startPos,endPos=endPos,startPos

        self.updatePositionalParams()
        self.setLine(LineF(startPos, endPos))
        self.update()


    def preSetPoints(self, startPos,endPos):
        self.orientation=HOEIZONTAL if startPos.y()==endPos.y() else VERTICAL
        if (startPos.y()>endPos.y()) or (startPos.x()>endPos.x() ):
            startPos,endPos=endPos,startPos
        self.updatePositionalParams()
        self.setLine(LineF(startPos, endPos))


    def compare(self,line):
        if self.orientation==line.orientation:
            if self.h==line.h :
                if line.r<self.l or self.r<line.l :
                    return CmpRes(CmpRes.NONE)
                elif line.r == self.l :
                    #getUnionNode(line,self)
                    setNode(self, line)
                    return CmpRes(CmpRes.NONE)
                elif self.r == line.l:
                    #getUnionNode(self, line)
                    setNode(self, line)
                    return CmpRes(CmpRes.NONE)
                else :
                    arr=(line.l,line.r,self.l,self.r)
                    l,r=min(arr),max(arr)
                    L=newLine( l, r,self.h, self.orientation)
                    return CmpRes(CmpRes.MATCH,[line , self],[L,])




        else :
            if   self.h==line.r or self.h==line.l:
                l,r=self.l, self.r
                if isContain(line.h, l, r):
                    L1 = newLine(l, line.h, self.h ,self.orientation)
                    L2 = newLine(line.h, r, self.h, self.orientation)
                    setNode(line,L1)
                    setNode(L1, L2,self.scene())
                    return CmpRes(CmpRes.CROSS,[self,],[L1,L2])
                elif isContact(line.h, l, r):
                    setNode(self, line)

            elif line.h==self.r or line.h==self.l:
                l,r=line.l, line.r
                if isContain(self.h, l, r):
                    L1 = newLine(l, self.h, line.h ,line.orientation)
                    L2 = newLine(self.h, r, line.h, line.orientation)
                    setNode(self,L1)
                    setNode(L1, L2,self.scene())
                    return CmpRes(CmpRes.CROSS,[line,],[L1,L2])
                elif isContact(self.h, l, r):
                    setNode(self, line)


        return CmpRes(CmpRes.NONE)

    def preRemove(self):
        self.left.remove()
        self.right.remove()

    def removeNode(self,node):
        if  self.right.node == node:
            self.right.clear()
        if self.left.node == node:
            self.left.clear()






class SceneItemPrototype(QtGui.QGraphicsRectItem,Proto):

    def __init__(self, *args, **kwargs):
        QtGui.QGraphicsRectItem.__init__(self, *args, **kwargs)
        self.setFlags(self.ItemIsSelectable )
        Proto.__init__(self, *args, **kwargs)

    def mouseMoveEvent(self, event):
        #print "m",event.scenePos()
        self.setPos(((event.scenePos()- self.deltaPos)/10).toPoint()*10)

    def paint(self, painter, option, widget):
        color = GREEN_COLOR if self.hover else BLACK_COLOR
        painter.setPen(QtGui.QPen(color, 2, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap, QtCore.Qt.BevelJoin))
        painter.drawRect(self.rect())