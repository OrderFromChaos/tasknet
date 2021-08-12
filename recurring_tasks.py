# Standard libraries
import json
import math
import sys
from pathlib import Path

# Pypi libraries
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import pendulum
import colour


class MainWindow(qtw.QWidget):

    def __init__(self, tasklist, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Recurring Task Tracker')
        self.setGeometry(800, 400, 900, 450)


        ### GUI settings
        newrow_breakpoint = 4 # Tasks per row before making a new one
        self.gradient_length = 50 # Number of hex colors in lateness gradient
        update_ms = 10 * 1000 # Number of milliseconds before updating task color
        self.N_length_in_seconds = 86_400 # What "N" means for interval (in seconds)


        # Setup layout
        overall_layout = qtw.QVBoxLayout()
        rows = []
        for i in range(math.ceil(len(tasklist) / newrow_breakpoint)):
            row = qtw.QHBoxLayout()
            rows.append(row)
            overall_layout.addLayout(row)
        self.tasklist = tasklist
        self.buttons = []

        taskComplete_factory = lambda i: (lambda: self.taskCompleted(i))
        for i, x in enumerate(tasklist):
            # Set up button and link to updateTask slot
            self.buttons.append(qtw.QPushButton(f'{x["name"]}'))
            self.buttons[i].clicked.connect(taskComplete_factory(i))

            # Add to layout
            rows[i // newrow_breakpoint].addWidget(self.buttons[i])
            # layout.addWidget(self.buttons[i])

        # Create color gradient
        start_color = colour.Color('lightgreen')
        end_color = colour.Color('red')
        self.intermediate_colors = list(start_color.range_to(end_color, self.gradient_length+1))

        # Set up rendering update timer
        timer = qtc.QTimer(self, interval = update_ms)
        timer.timeout.connect(self.updateColors)
        timer.start()
        self.updateColors()

        # Final prep/show window
        self.setLayout(overall_layout)
        self.show()

    @qtc.pyqtSlot(int)
    def taskCompleted(self, taskID):
        relevant_task = self.tasklist[taskID]
        print(f'Task "{relevant_task["name"]}" completed!')
        relevant_task['start'] = pendulum.now()

    def updateColors(self):
        for task, button in zip(self.tasklist, self.buttons):
            if task['recurrence_type'] == 'interval':

                task_sec = task['N']
                percentage_complete = max(
                    0,
                        min(
                        1,
                        (
                            (pendulum.now() - task['start']).total_seconds()) / self.N_length_in_seconds
                            / task_sec
                        )
                    )
                intermediate_index = int(round(percentage_complete * self.gradient_length, 0))

                curr_color = qtg.QColor(self.intermediate_colors[intermediate_index].hex_l)
                button.setStyleSheet(f"background-color: {curr_color.name()}")


if __name__ == '__main__':
    recurring_tasks_path = Path('data/recurring_tasks.json')

    with open(recurring_tasks_path, 'r') as f:
        tasks = json.load(f)
    for t in tasks:
        if t['recurrence_type'] == 'interval':
            t['start'] = pendulum.parse(t['start'])

    app = qtw.QApplication(sys.argv)
    w = MainWindow(tasks)
    return_code = app.exec_()

    # Write updated task completion dates
    output_tasklist = w.tasklist
    for t in output_tasklist:
        if t['recurrence_type'] == 'interval':
            t['start'] = str(t['start'])
    with open(recurring_tasks_path, 'w') as f:
        json.dump(w.tasklist, f, indent=4)

    sys.exit(return_code)