from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import math
from things.Cell import Cell
from collections import  deque
import sys

class Window(QMainWindow):
    '''
        Recursive BAckTacker
    '''
    def __init__(self, width=800, height=800, top=150, left=150):
        super().__init__()
        self.title = "PyQt5 Drawing Rectangle"
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.InitWindow()
        self.grid = []
        self.w = 40
        self.rows = math.floor(self.width/self.w)
        self.columns = math.floor(self.width/self.w)
        self.myStaxk = deque()
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(Cell(i,j))
            self.grid.append(row)
        self.myStaxk.append(self.grid[0][0])

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for cell_list in self.grid:
            for cell in cell_list:
                cell.init_grid(painter, self.w)

        while len(self.myStaxk) > 0:
            ccell = self.myStaxk.pop()
            self.current = ccell;




App = QApplication(sys.argv)
window = Window(600,600)
sys.exit(App.exec())
