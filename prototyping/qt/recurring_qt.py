from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMainWindow
)
from PyQt5.QtGui import (
    QColor
)
from PyQt5.QtCore import (
    QTimer,
    Qt,
    QThread,
    QRunnable,
    QThreadPool,
    pyqtSlot
)
import sys
import time
import random


# Use this:
# https://pythonspot.com/pyqt5-colors/


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'recurring'
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle(self.title)
        self.setAutoFillBackground(True)

        # Draw task
        self.taskarray = [
            ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
            ['Task 5', 'Task 6', 'Task 7', 'Task 8'],
            ['Task 9', 'Task 10', 'Task 11', 'Task 12'],
            ['Task 13', 'Task 14', 'Task 15', 'Task 16']
        ]
        self.verts = QVBoxLayout()
        horiz = []
        self.button_objs = []
        for taskrow in self.taskarray:
            horiz.append(QHBoxLayout()) # TODO: Keep inside a vert into a horiz instead; vertical breaks are less annoying than horizontal breaks
            curr_UI_row = horiz[-1]
            for taskname in taskrow:
                button = QPushButton(taskname)
                self.button_objs.append(button)
                curr_UI_row.addWidget(self.button_objs[-1])
            self.verts.addLayout(curr_UI_row)

        # Draw onto existing window
        self.window = QWidget(self)
        self.setCentralWidget(self.window)

        self.window.setLayout(self.verts)

        self.show()

        pool = QThreadPool.globalInstance()
        print(f'{pool.maxThreadCount()=}')
        cu = ColorUpdater(0, self.button_objs)
        pool.start(cu)

        # https://stackoverflow.com/questions/1386043/how-to-make-qt-work-when-main-thread-is-busy


class ColorUpdater(QRunnable):

    def __init__(self, n, button_objs):
        super().__init__()
        self.n = n
        self.button_objs = button_objs

    def run(self):
        while True:
            print('Run loop...')
            time.sleep(1000)
            for button in self.button_objs:
                if random.randint(1, 100) < 50:
                    button.setStyleSheet(
                        'background-color: green'
                    )
                else:
                    button.setStyleSheet(
                        'background-color: yellow'
                    )
            break



if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
