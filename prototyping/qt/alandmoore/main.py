import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as gtg
from PyQt5 import QtWidgets as qtw

class MainWindow(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = qtw.QHBoxLayout()
        buttons = []

        fxn_factory = lambda i: (lambda: self.updateTask(i+1))
        for i in range(10):
            buttons.append(qtw.QPushButton(f'Task {i+1}'))
            buttons[i].clicked.connect(fxn_factory(i))
            layout.addWidget(buttons[i])

        button_parent = qtw.QWidget()
        button_parent.setLayout(layout)
        self.setLayout(layout)

        self.show()

    def updateTask(self, taskID):
        print(f'Task {taskID} completed!')



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = MainWindow(windowTitle = 'hello world')
    sys.exit(app.exec_())