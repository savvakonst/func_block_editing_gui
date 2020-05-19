

from PyQt4 import QtGui, QtCore
from enum import Enum

def dbg(txt):
    #print txt
    pass

def item_proto_init(self):
    self.setAcceptHoverEvents(True)
    self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)


VERTICAL=True
HOEIZONTAL=False




BLACK_COLOR=QtCore.Qt.black
RED_COLOR=QtGui.QColor("#ff0000")
GREEN_COLOR=QtGui.QColor("#008f00")
VIOLET_COLOR= QtGui.QColor("#7d0779")
BLUE_COLOR= QtGui.QColor("#0000eb")

MAIN_LINE_COLOR=VIOLET_COLOR
SUB_LINE_COLOR=BLUE_COLOR

SUB_LINE_STYLE=QtCore.Qt.SolidLine#QtCore.Qt.DashLine
MAIN_LINE_STYLE=QtCore.Qt.SolidLine



IDLE_STATE=0
LINE_ON_MOVE_STATE=1
LINE_ON_DRAW_STATE=2

LINE_t=6
NODE_t=4




class MODE(Enum):
    ARROW_MODE = 0
    LINE_MODE = 1
    ELEMENT_MODE = 2