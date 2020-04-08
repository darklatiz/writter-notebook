from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import math
from things.Cell import Cell
import sys

class Window(QMainWindow):
    '''
        Recursive BAckTacker
    '''
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Rectangle"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 800
        self.InitWindow()
        self.grid = []
        self.w = 40
        self.rows = math.floor(self.width/self.w)
        self.columns = math.floor(self.width/self.w)
        for i in range(self.rows):
            for j in range(self.columns):
                self.grid.append(Cell(i,j))
        self.current = self.grid[0]
        self.current.visited = True

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        #(int x, int y, int width, int height)
        for cell in self.grid:
            #painter.drawRect(cell.row * self.w, cell.col * self.w, self.w, self.w)
            cell.show(painter, self.w)



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
