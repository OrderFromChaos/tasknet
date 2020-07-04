# Idea: use a similar scrollback effect as capturing, but up instead of down
# Pressing "u" lets you undo a data entry
# Take the question interface from old/tsk.py
# Keep a "lines" array in history
# Two windows - entry and edit

# Internal libraries
from core.dataclasses import *
from core.dbinterface import *
from core.utility import validate_input
from core.customtextbox import CustomTextbox

# Standard libraries
from collections import OrderedDict

class clarifying:
    def __init__(self, context):
        self.context = context
        self.edithistory = []
        self.lines = []
        self.exiturl = 'mainmenu'
        self.tasks = OrderedDict()
    def show(self, mainscreen):
        max_y, max_x = mainscreen.getmaxyx()
        
        scrollwindow = curses.newwin(20, max_x, 0, 0)
        editwindow = curses.newwin(4, max_x, 21, 0)
        
        # Figure out which tasks need clarifying
        # Needs clarifying:
            # Missing do by/due date
            # Missing expected length (needed for autoscheduling)
            # Not tagged as at bottom of subtask detail (optional; config in settings)
        self.tasks = readTasks(self.context, 'todo')
        for uid, taskobj in self.tasks.items():
            conditions = [
                lambda x: x.doby or x.duedate, # Due date
                lambda x: x.expectedlength,    # Expected length
                lambda x: x.leaftag            # Tagged by user as being maximally detailed
            ]
            self.tasks[uid].needsclarify = [f(taskobj) for f in conditions]

        for uid, taskobj in self.tasks.items():
            

        return {'url': self.exiturl()}
