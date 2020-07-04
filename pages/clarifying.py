# Idea: use a similar scrollback effect as capturing, but up instead of down
# Pressing "u" lets you undo a data entry
# Take the question interface from old/tsk.py
# Keep a "lines" array in history
# Two windows - entry and edit

from core.dataclasses import *
from core.dbinterface import *
from core.utility import validate_input
from core.customtextbox import CustomTextbox

class clarifying:
    def __init__(self, context):
        self.context = context
        self.edithistory = []
        self.lines = []
        self.exiturl = 'mainmenu'
    def show(self, mainscreen):
        max_y, max_x = mainscreen.getmaxyx()
        
        scrollwindow = curses.newwin(20, max_x, 0, 0)
        editwindow = curses.newwin(4, max_x, 21, 0)
        
        while True:
            

        return {'url': self.exiturl()}
