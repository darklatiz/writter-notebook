import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, qApp, QAction, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QPoint
import math
from things.Cell import Cell
from collections import deque
import random
import time
import sys


class MazeGenerator(QMainWindow):
    '''
        Recursive BAckTacker
    '''

    def __init__(self, width=900, height=900, weight=3, top=150, left=150):
        QMainWindow.__init__(self)
        self.title = "PyQt5 Drawing Rectangle"
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.grid = None
        self.w = weight
        self.init_window()
        self.rows = math.floor(self.width / self.w)
        self.columns = math.floor(self.width / self.w)
        self.back_tracker = deque()
        self.path = []
        self.current = None
        self.func = (None, None)
        self.grid_painted = False

        self.grid = self.__create_2d_array(self.rows, self.columns)

        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j] = Cell(i, j)
        self.back_tracker.append(self.grid[math.floor(self.rows / 2) + 1][math.floor(self.columns / 2)])

        self.func = (None, None)
        self.mModified = True

        # self.create_actions()
        # self.create_tool_bars()

    def init_window(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def create_actions(self):
        root = PyQt5.QtCore.QFileInfo(__file__).absolutePath()

        self.new_maze = QAction(QIcon(root + '/images/new.png'), "&Create Maze", self,
                                shortcut=QKeySequence.New, statusTip="Start Maze Creation",
                                triggered=self.create_maze)

        self.save_as_action = QAction(QIcon(root + '/images/save.png'), "Save &As...", self,
                                      shortcut=QKeySequence.SaveAs,
                                      statusTip="Save the document under a new name",
                                      triggered=self.save_as)

        self.exit_action = QAction(QIcon(root + '/images/exit.png'), "&Exit", self, shortcut="Ctrl+Q",
                                   statusTip="Exit the application", triggered=self.close)

        self.about_action = QAction(QIcon(root + '/images/about.png'), "&About", self,
                                    statusTip="Show the application's About box",
                                    triggered=self.about)

    def create_tool_bars(self):
        self.create_bar = self.addToolBar("Create Maze")
        self.create_bar.addAction(self.new_maze)
        self.create_bar.addAction(self.save_as_action)

        self.about_bar = self.addToolBar("About")
        self.about_bar.addAction(self.exit_action)
        self.about_bar.addAction(self.about_action)

    def paintEvent(self, e):
        print("paint EVEnT >>>>>>>>>>>>")
        if self.mModified:
            self.mModified = False

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))

        if not self.grid_painted:
            for cell_list in self.grid:
                for cell in cell_list:
                    cell.init_grid(painter, self.w)
            # self.grid_painted = True

        self.draw_path(painter)
        self.sent_painter(painter)
        painter.end()

    def sent_painter(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["painter"] = qp
            func(**kwargs)

    def create_maze(self, painter):
        while len(self.back_tracker) > 0:
        # for i in range(1):
            if len(self.back_tracker) > 0:
                c_cell = self.back_tracker.pop()
                self.current = c_cell
                print("Current {0}".format(c_cell))
                c_cell.visited = True
                self.path.append(c_cell)
                c_cell.draw_mark(painter, self.w)
                c_cell.check_neighbours(self.grid)
                not_visited_cells = [visited_cell for visited_cell in c_cell.neighbours if not visited_cell.visited]

                if len(not_visited_cells) > 0:
                    # print("Pushing {0}".format(self.current))
                    self.back_tracker.append(self.current)
                    # verify the neighbours that have not been visited
                    len_n = len(not_visited_cells)
                    if len_n > 1:
                        random_index = random.randrange(0, len_n)
                    else:
                        random_index = 0

                    n_cell = not_visited_cells[random_index]
                    n_cell.visited = True
                    # print("Pushing {0}".format(n_cell))
                    self.remove_walls(self.current, n_cell)
                    self.back_tracker.append(n_cell)
            else:
                print("Finisehd.........")
                for x in range(len(self.grid)):
                    for y in range(len(self.grid[x])):
                        c = self.grid[x][y]
                        print('Cell ({0},{1}), visited= {2}'.format(c.row, c.col, c.visited))

    def draw_path(self, painter):
        for cell in self.path:
            painter.setPen(Qt.NoPen)
            # painter.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(cell.col * self.w, cell.row * self.w, self.w, self.w)

    def remove_walls(self, current_cell, next_cell):
        pos_current = current_cell.col + self.columns * current_cell.row
        pos_next = next_cell.col + self.columns * next_cell.row

        # we are in the same row so subtracts cols
        if current_cell.row == next_cell.row:
            relative_col_pos = current_cell.col - next_cell.col
            if relative_col_pos == 1:
                current_cell.walls["left"] = None
                next_cell.walls["right"] = None
            elif relative_col_pos == -1:
                current_cell.walls["right"] = None
                next_cell.walls["left"] = None
        elif current_cell.col == next_cell.col:
            relative_row_pos = current_cell.row - next_cell.row
            if relative_row_pos == 1:
                current_cell.walls["top"] = None
                next_cell.walls["bottom"] = None
            elif relative_row_pos == -1:
                current_cell.walls["bottom"] = None
                next_cell.walls["top"] = None

    def save_as(self):
        print("to be implemented")

    def about(self):
        QMessageBox.about(self, "About Application",
                          "The <b>Application</b> Maze Creation.")

    def keyPressEvent(self, event):
        gey = event.key()
        self.func = (None, None)
        if gey == Qt.Key_M:
            print("Key 'm' pressed!")
        elif gey == Qt.Key_Right:
            print("Right key pressed!, call drawFundBlock()")
            self.func = (self.create_maze, {})
            self.mModified = True
            self.update()
        elif gey == Qt.Key_5:
            print("#5 pressed, call drawNumber()")
            self.func = (self.drawNumber, {"notePoint": QPoint(100, 100)})
            self.mModified = True
            self.update()

    def __create_2d_array(self, rows, cols):
        return [[0] * cols for i in range(rows)]


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    maze_generator = MazeGenerator()
    sys.exit(app.exec_())
