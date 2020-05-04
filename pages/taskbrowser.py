# needs to accept recursive todos
# display todo information on the side
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

from core.dbinterface import *
from collections import deque
from ordered_set import OrderedSet

class taskbrowser:
    def __init__(self, context):
        self.context = context
        self.tasks = self.getContent()

    def show(self, mainscreen):
        # make two windows;
        # left for name info,
        # right for metadata

        # TODO: Account for 0 tasks

        while True:
            ### 1. Left window

            # Observation: the first element of todo.json is
            #       always guaranteed to be a top level task
            todisplay = OrderedSet(self.tasks.keys())
            d = deque()
            d.append((todisplay[0], 0))

            row = 2
            while todisplay:
                if d:
                    curr, depth = d.popleft()
                else:
                    curr, depth = todisplay[0], 0
                todisplay.remove(curr)
                elt = self.tasks[curr]

                mainscreen.addstr(row, 2+depth, elt.name)
                row += 1
                if elt.children:
                    for i in elt.children:
                        d.append((i, depth+1))

            userinput = mainscreen.getch()
            if userinput == ord('q'):
                break
            
        return {'url': 'mainmenu'}

    def getContent(self):
        return readTasks(self.context, 'todo')
