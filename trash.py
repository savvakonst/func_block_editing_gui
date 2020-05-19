from PyQt4 import QtGui, QtCore




def item_proto_init(self):
    self.setAcceptHoverEvents(True)
    self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)


class Item():
    pass

class LineGroup():
    pass

class Line():

    def addPointSegment(self):
        pass

    def internal_init(self):
        self.selected_items=[]

    def moveSelectedItems(self,incrPos):
        for i in self.selected_items:
            pass


class Scene():
    def internal_init(self):
        self.selected_items=[]
    def moveSelectedItems(self,incrPos):
        for i in self.selected_items:
            pass






def getUnionNode(left,right):
    if left.right.node is None or right.left.node is None :
        #print "getUnionNode"
        node=Node( [left,right], newPoint(right.l ,right.h ,right.orientation) )
        node.type_=Node.UNION
        left.right.node,right.left.node =node,node
        left.scene().nodes.add(node)
        return node
    if left.right.node == right.left.node :
        return left.right.node
    else:
        #print ("error getUnionNode")
        return None