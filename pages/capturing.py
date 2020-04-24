from core.dataclasses import *
from core.dbinterface import *

class capturing:
    def __init__(self):
        self.tasklist = [] # Needs to be initialized during show step 
                           # due to limitations on "context" knowledge

    def show(self, screen, context):
        self.getTaskList(context, 'todo')

        t = Task('Apply for a job',
                 doby=datetime(2020, 4, 30)
                 )

        self.tasklist.append(t)
        
        self.writeTaskList(context, 'todo')

        return {'url': 'mainmenu'}

    def getTaskList(self, context, filename):
        self.tasklist = readTasks(context, filename)

    def writeTaskList(self, context, filename):
        writeTasks(self.tasklist, context, filename)
