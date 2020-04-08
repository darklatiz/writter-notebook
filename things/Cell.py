from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush


class Cell:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {
            "left": True,
            "right": True,
            "top": True,
            "bottom": True
        }

    def show(self, painter, w):
        x = self.row * w
        y = self.col * w
        # top
        if self.walls["top"]:
            painter.drawLine(x, y, x + w, y)

        # right
        if self.walls["right"]:
            painter.drawLine(x + w, y, x + w, y + w)

        # bottom
        if self.walls["bottom"]:
            painter.drawLine(x + w, y + w, x, y + w)

        # left
        if self.walls["left"]:
            painter.drawLine(x, y + w, x, y)

        if self.visited:
            painter.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
            painter.drawRect(self.row * w, self.col * w, w, w)
