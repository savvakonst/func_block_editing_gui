
import sys
if sys.version_info[0] >= 3:
    xrange = range

import constants as co


class Point():
    x:int
    y:int
    def __init__(self,x : int =0,y : int =0):
        self.x,self.y=int(x),int(y)

    def __add__(self, other : 'Point') -> 'Point':
        x, y = self.x + other.x, self.y + other.y
        return Point(x,y)

    def __sub__(self, other : 'Point') -> 'Point':
        x, y = self.x - other.x, self.y - other.y
        return Point(x,y)

    def __iadd__(self, other : 'Point') -> 'Point':
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other : 'Point') -> 'Point':
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other) -> 'Point':
        if isinstance(other, int) :
            x, y = self.x * other, self.y * other
            return Point(x, y)
        elif isinstance(other, Point) :
            x, y = self.x * other.x, self.y * other.y
            return Point(x,y)

    def __eq__(self, other : 'Point') -> bool:
        return (self.x == other.x ),(self.y == other.y)

    def __str__(self):
        return'Point({:d},{:d})'.format(self.x,self.y)


class Line():

    def __init__(self,L=Point(),R=Point()):
        self.pointL=Point()
        self.pointR=Point()
        eqX,eqY=self.pointL == self.pointR
        if eqX and eqY: self.orientation = co.NONE
        elif eqY:       self.orientation = co.HORIZONTAL
        elif eqX:       self.orientation = co.VERTICAL
        else :          raise  Exception("invalid points")
        self.orderPoints()

    def __iadd__(self, other : 'Point') -> 'Line':
        if isinstance(other, Point) :
            self.pointL+=other
            self.pointR+=other
        else:
            raise Exception("invalid arg");
        return self

    def __eq__(self, other : 'Line') -> bool:
        return self.orientation==other.orientation


    def __contains__(self, point : 'Point') -> bool:
        if self.orientation == co.HORIZONTAL:
            if ( self.pointL.x < point.x) and ( point.x < self.pointR.x):
                return ((self.pointL.y-co.DELTA )< point.y) and ( point.y < (self.pointL.y+co.DELTA ))
        elif self.orientation == co.VERTICAL:
            if ( self.pointL.y < point.y) and ( point.y < self.pointR.y):
                return ((self.pointL.x-co.DELTA )< point.x) and ( point.x < (self.pointL.x+co.DELTA ))
        else: raise Exception("match");


    def orderPoints(self):
        if self.orientation == co.HORIZONTAL :
            self.pointL,self.pointR = (self.pointL,self.pointR)if self.pointL.x<self.pointR.x else (self.pointR,self.pointL)
        if self.orientation == co.VERTICAL :
            self.pointL,self.pointR = (self.pointL,self.pointR)if self.pointL.y<self.pointR.y else (self.pointR,self.pointL)

    def isZeroLen(self):
        return self.pointL==self.pointR

    def clear(self):
        pass

    def clearIfZero(self):
        if self.isZeroLen():
            self.clear();
            return True
        return False


    def calcH(self):
        if self.orientation == co.HORIZONTAL:self.h = self.pointL.y
        elif self.orientation == co.VERTICAL:self.h = self.pointL.x
        else: raise Exception("calcH");

    def calcL(self):
        if self.orientation == co.HORIZONTAL:self.l = self.pointL.x
        elif self.orientation == co.VERTICAL:self.l = self.pointL.y
        else: raise Exception("calcL");

    def calcR(self):
        if self.orientation == co.HORIZONTAL:self.r = self.pointR.x
        elif self.orientation == co.VERTICAL:self.r = self.pointR.y
        else: raise Exception("calcR");


    def h(self)-> 'Line':
        self.calcH()
        return self.h

    def l(self)-> 'Line':
        self.calcL()
        return self.l

    def r(self)-> 'Line':
        self.calcR()
        return self.r






def newLine(l,r,h,orientation):
    if orientation==co.HORIZONTAL :
        return Line(Point(l,h),Point(r,h))
    elif orientation==co.VERTICAL :
        return Line(Point(h,l),Point(h,r))

    return None

def isContain(p,l,r):
    return (l<p and p<r)

def isContact(p,l,r):
    return (l==p) or (p==r)

class Scene():

    lineList : list

    def __init_(self,viewFrame=None):
        #QtGui.QGraphicsView()
        self.lineList=[]

    def removeZeroLenLines(self):
        for i in self.lineList:
            if i.isZeroLen(): i.remove()
        self.lineList = list( filter(lambda x: not i.clearIfZero()  ,self.lineList ))

    def compareFirstStage(self,firstLine,list,index):
        secondLine=list[index]

        if firstLine.orientation==secondLine.orientation:
            if firstLine.h()==secondLine.h() :
                if secondLine.r()<firstLine.pointL or firstLine.r()<secondLine.pointL :
                    return co.NONE
                elif secondLine.r() == firstLine.l() :
                    return co.NONE
                elif firstLine.r() == secondLine.l() :
                    return co.NONE
                else :
                    arr=(secondLine.l(),secondLine.r(),firstLine.l(),firstLine.r())
                    l,r=min(arr),max(arr)
                    secondLine.clear();firstLine.clear();
                    list[index]=newLine( l, r,firstLine.h(), firstLine.orientation)
                    return co.OVERLAP

        else:
            if firstLine.h()==secondLine.r() or firstLine.h()==secondLine.l():
                l,r=firstLine.l(), firstLine.r()
                if isContain(secondLine.h(), l, r):
                    list[index] = newLine(l, secondLine.h(), firstLine.h(), firstLine.orientation)
                    list.append(  newLine(secondLine.h(), r, firstLine.h(), firstLine.orientation))
                    firstLine.clear()
                    return co.CROSS
                elif isContact(secondLine.h(), l, r):
                    return co.NONE

            elif secondLine.h()==firstLine.r() or secondLine.h()==firstLine.l():
                l,r=secondLine.l(), secondLine.r()
                if isContain(firstLine.h(), l, r):
                    list[index] = newLine(l, firstLine.h(), secondLine.h() ,secondLine.orientation)
                    list.append(  newLine(firstLine.h(), r, secondLine.h(), secondLine.orientation))
                    secondLine.clear()
                    return co.CROSS
                elif isContact(firstLine.h(), l, r):
                    return co.NONE

        return co.NONE



    def getItem(self,point: Point)->list:
        list=[]
        for i in self.lineList :
            if point in i :
                list.append(i)
        return list

    def refactoring(self):

        tempLineList=[i for i in self.lineList]
        self.lineList=[]

        while len(tempLineList):
            line=tempLineList.pop()
            cond = True
            for index in xrange(len(tempLineList)):
                if self.compareFirstStage(line,tempLineList,index)!=co.NONE:
                    cond = False
                    break
            if cond :
                self.lineList.append(line)


    def mouseEvent(self,event_ty, pos: Point):
        if event_ty==co.PRESS:
            pass



    def plot(self):
        pass

