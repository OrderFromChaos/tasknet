import sys, math, random
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut
from PyQt5.QtGui import QPainter, QPen, QColor, QKeySequence
from PyQt5.QtCore import Qt, QTimer, QThread

WIDTH = 40
grid = []

class Cell():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [1, 1, 1, 1]  # top, right, bottom, left
        self.visited = 0
        self.currentCell = 0

    def index(self, i, j, cols, rows):
        if (i < 0) or (j < 0) or (i > (cols - 1)) or (j > (rows - 1)):
            return None
        else:
            return i + j * cols

    def checkNeighbors(self, cols, rows):
        neighbors = []
        if not (self.index(self.i, self.j - 1, cols, rows) is None):
            top    = grid[self.index(self.i, self.j - 1, cols, rows)]
        if not (self.index(self.i + 1, self.j, cols, rows) is None):
            right  = grid[self.index(self.i + 1, self.j, cols, rows)]
        if not (self.index(self.i, self.j + 1, cols, rows) is None):
            bottom = grid[self.index(self.i, self.j + 1, cols, rows)]
        if not (self.index(self.i - 1, self.j, cols, rows) is None):
            left   = grid[self.index(self.i - 1, self.j, cols, rows)]
        if 'top' in locals() and not top.visited:
            neighbors.append(top)
        if 'right' in locals() and not right.visited:
            neighbors.append(right)
        if 'bottom' in locals() and not bottom.visited:
            neighbors.append(bottom)
        if 'left' in locals() and not left.visited:
            neighbors.append(left)
        if len(neighbors) > 0:
            r = math.floor(random.uniform(0, len(neighbors)))
            return neighbors[r]
        else:
            return None


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.cols = math.floor(self.width / WIDTH)
        self.rows = math.floor(self.height / WIDTH)
        self.active = False
        self.initui()
        self.init_cells()

    def init_cells(self):
        if not self.active:
            del grid[:]
            for j in range(self.rows):
                for i in range(self.cols):
                    cell = Cell(i, j)
                    grid.append(cell)
            QTimer.singleShot(1, self.go)

    def go(self):
        self.active = True
        current = grid[0]
        current.visited = 1
        current.currentCell = 1
        while True:
            self.update()
            QApplication.processEvents()
            QThread.msleep(150)
            next = current.checkNeighbors(self.cols, self.rows)
            if next is not None:
                next.visited = 1
                next.currentCell = 1
                current.currentCell = 0
                current = next
            else:
                break
        self.active = False

    def initui(self):
        QShortcut(QKeySequence('F5'), self, self.init_cells)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.show()

    def paintEvent(self, e):
        for i in grid:
            self.draw_cell(i)

    def draw_cell(self, cell):
        x = cell.i * WIDTH
        y = cell.j * WIDTH
        # LINES
        qp = QPainter(self)
        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        if cell.walls[0]:  # top
            qp.drawLine(x    , y    , x + WIDTH, y)
        if cell.walls[1]:  # right
            qp.drawLine(x + WIDTH, y    , x + WIDTH, y + WIDTH)
        if cell.walls[2]:  # bottom
            qp.drawLine(x + WIDTH, y + WIDTH, x    , y + WIDTH)
        if cell.walls[3]:  # left
            qp.drawLine(x    , y + WIDTH, x    , y)
        if cell.visited:
            if cell.currentCell:
                qp.setBrush(QColor(0, 255, 0, 255))
            else:
                qp.setBrush(QColor(255, 0, 255, 100))
            qp.drawRect(x, y, WIDTH, WIDTH)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())