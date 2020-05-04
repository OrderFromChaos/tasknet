# needs to accept recursive todos
# display todo information on the side
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

from core.dbinterface import *
from collections import deque

class taskbrowser:
    def __init__(self, context):
        self.context = context
        self.tasks = self.getContent()
        self.taskcount = 5 # Determine task count
        # TODO: Rewrite data storage to use unique IDs

    def show(self, mainscreen):
        while True:
            # make two windows;
            # left for name info,
            # right for metadata

            # left window
            row = 2
            d = deque()
            for entry in self.tasks:
                d.append((entry,0))
                while len(d):
                    top, depth = d.popleft()
                    mainscreen.addstr(row, 2+depth, top.name)
                    row += 1
                    if top.children:
                        for i in top.children:
                            top.append((i, depth+1))

            userinput = mainscreen.getch()
            if userinput == ord('q'):
                break
            
        return {'url': 'mainmenu'}

    def getContent(self):
        return readTasks(self.context, 'todo')
