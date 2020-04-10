from builtins import IndexError

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
        print("Visitado {0}".format(self.visited))
        if self.visited:
            painter.setBrush(QBrush(Qt.darkMagenta, Qt.SolidPattern))
            painter.drawRect(self.row * w, self.col * w, w, w)

    def check_neighbours(self, the_grid, the_stack):
        ramdom_if = random.randrange(4)

        if ramdom_if == 0:
            print("Random if 0")
            cell_top    = self.get_cell_from_grid(the_grid, self.row, self.col - 1)
            if cell_top is not None and not cell_top.visited:
                the_stack.append(cell_top)
        elif ramdom_if == 1:
            print("Random if: 1")
            cell_right  = self.get_cell_from_grid(the_grid,self.row + 1, self.col)
            if cell_right is not None and not cell_right.visited:
                the_stack.append(cell_right)
        elif ramdom_if == 2:
            print("Random if: {0}".format(ramdom_if))
            cell_bottom = self.get_cell_from_grid(the_grid, self.row, self.col + 1)
            if cell_bottom is not None and not cell_bottom.visited:
                the_stack.append(cell_bottom)
        elif ramdom_if == 3:
            print("Random if: {0}".format(ramdom_if))
            cell_left   = self.get_cell_from_grid(the_grid, self.row - 1, self.col)
            if cell_left is not None and not cell_left.visited:
                the_stack.append(cell_left)
        '''
        if len(self.neighbours) > 0:
            print("Vecinos: {0}".format(self.neighbours))
            index = random.randrange(4)
            print("Vecino en index {0}".format(index))
            try:
                return self.neighbours[index]
            except IndexError as e:
                return None
        else:
            return None
        '''

    def get_cell_from_grid(self, the_grid, row, col):
        try:
            return the_grid[row][col]
        except IndexError as indexerr:
            print("Error en cell({0},{1})".format(row, col))
            return None

    def __str__(self):
        return "Cell({0},{1})".format(self.row,self.col)
