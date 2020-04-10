from builtins import IndexError

from PyQt5.QtCore import Qt, QLine
from PyQt5.QtGui import QBrush
import random


class Cell:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.loaded_neighbours = False
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
        print("Visitado {0}".format(self.visited))
        if self.visited:
            painter.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
            painter.drawRect(self.row * w, self.col * w, w, w)

    def check_neighbours(self, the_grid):
        if not self.loaded_neighbours:
            self.get_neighbours_from_grid(the_grid)
        else:
            print("Neighbours have been loaded")

    def get_neighbours_from_grid(self, the_grid):
        try:
            #top
            c = the_grid[self.row][self.col -1]
            if not c.visited:
                self.neighbours.append(c)
        except IndexError as indexerr:
            print("Neighbour not found cell({0},{1})".format(self.row, self.col -1))


        try:
            #right
            c = the_grid[self.row + 1][self.col]
            if not c.visited:
                self.neighbours.append(c)
        except IndexError as indexerr:
            print("Neighbour not found cell({0},{1})".format(self.row + 1, self.col))

        try:
            #bottom
            c = the_grid[self.row][self.col + 1]
            if not c.visited:
                self.neighbours.append(c)
        except IndexError as indexerr:
            print("Neighbour not found cell({0},{1})".format(self.row, self.col + 1))

        try:
            #left
            c = the_grid[self.row - 1][self.col]
            if not c.visited:
                self.neighbours.append(c)
        except IndexError as indexerr:
            print("Neighbour not found cell({0},{1})".format(self.row - 1, self.col))



    def __str__(self):
        return "Cell({0},{1})".format(self.row,self.col)
