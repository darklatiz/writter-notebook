from PyQt5.QtCore import Qt, QLine
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

    def init_grid(self, painter, w):
        x = self.row * w
        y = self.col * w

        # top
        line_top = QLine(x, y, x + w, y)
        painter.drawLine(line_top)
        self.walls["top"] = line_top

        # right
        line_right = QLine(x + w, y, x + w, y + w)
        painter.drawLine(line_right)
        self.walls["right"] = line_right

        # bottom
        line_bottom = QLine(x + w, y + w, x, y + w)
        painter.drawLine(line_bottom)
        self.walls["bottom"] = line_bottom

        # left
        line_left = QLine(x, y + w, x, y)
        painter.drawLine(line_left)
        self.walls["left"] = line_left

        if self.visited:
            painter.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
            painter.drawRect(self.row * w, self.col * w, w, w)

    def check_neighbours(self, top, right, bottom, left):
        neighbours = []
