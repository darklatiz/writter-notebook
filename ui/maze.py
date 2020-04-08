from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
import math
from things.Cell import Cell
import sys

class Window(QMainWindow):
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
            x = cell.row * self.w
            y = cell.col * self.w
            #painter.drawRect(cell.row * self.w, cell.col * self.w, self.w, self.w)

            #top
            if cell.walls["top"]:
                painter.drawLine(x         , y         , x + self.w, y)

            #right
            if cell.walls["right"]:
                painter.drawLine(x + self.w, y         , x + self.w, y + self.w)

            #bottom
            if cell.walls["bottom"]:
                painter.drawLine(x + self.w, y + self.w, x         , y + self.w)

            #left
            if cell.walls["left"]:
                painter.drawLine(x         , y + self.w, x         , y)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
