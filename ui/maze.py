import PyQt5
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, qApp, QAction, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QPoint
import math
from things.Cell import Cell
from collections import  deque
import sys

class MainWindow(QMainWindow):
    '''
        Recursive BAckTacker
    '''
    def __init__(self, width=800, height=800, top=150, left=150):
        QMainWindow.__init__(self)
        self.title = "PyQt5 Drawing Rectangle"
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.grid = []
        self.w = 40
        self.init_window()
        self.rows = math.floor(self.width/self.w)
        self.columns = math.floor(self.width/self.w)
        self.myStaxk = deque()
        self.current = None
        self.func = (None, None)
        self.grid_painted = False
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(Cell(i,j))
            self.grid.append(row)
        self.myStaxk.append(self.grid[0][0])
        self.grid[0][0].visited = True

        self.func = (None, None)
        self.mModified = True

        self.create_actions()
        self.create_tool_bars()

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

        self.about_action = QAction(QIcon(root + '/images/about.png'),"&About", self,
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
            #self.grid_painted = True

        self.sent_painter(painter)

    def sent_painter(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["painter"] = qp
            func(**kwargs)

    def create_maze(self, painter):
        #while len(self.myStaxk) > 0:
        for i in range(1):
            c_cell = self.myStaxk.pop()
            self.current = c_cell;
            c_cell.visited = True
            c_cell.draw_mark(painter, self.w)
            unvisited_cell = c_cell.check_neighbours(self.grid)
            if unvisited_cell is not None:
                print(type(unvisited_cell))
                print("({0}, {1})".format(unvisited_cell.col, unvisited_cell.row))
                self.myStaxk.append(unvisited_cell)

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


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    #mainWin.show()
    sys.exit(app.exec_())
