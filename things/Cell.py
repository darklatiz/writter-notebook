from PyQt5.QtCore import Qt, QLine
from PyQt5.QtGui import QBrush
import random


class Cell:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.neighbours = []
        self.walls = {
            "left": None,
            "right": None,
            "top": None,
            "bottom": None
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


    def draw_mark(self, painter, w):
        if self.visited:
            painter.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
            painter.drawRect(self.row * w, self.col * w, w, w)

    def check_neighbours(self, the_grid):
        #we get top right bottom left
        #random.choice("top", "right", "bottom", "left")

        cell_top    = the_grid[self.row][self.col - 1]
        if cell_top is not None and not cell_top.visited:
            self.neighbours.append(cell_top)

        cell_right  = the_grid[self.row + 1][self.col]
        if cell_right is not None and not cell_right.visited:
            self.neighbours.append(cell_right)

        cell_bottom = the_grid[self.row][self.col + 1]
        if cell_bottom is not None and not cell_bottom.visited:
            self.neighbours.append(cell_bottom)

        cell_left   = the_grid[self.row - 1][self.col]
        if cell_left is not None and not cell_left.visited:
            self.neighbours.append(cell_left)

        if len(self.neighbours) > 0:
            index = random.randrange(4)
            return self.neighbours[index]
        else:
            return None
