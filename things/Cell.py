
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
