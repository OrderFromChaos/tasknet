from core.dataclasses import *
from core.dbinterface import *
from pages.common import *
import re # Input validation

class capturing(inputWithScrollBack):
    def __init__(self):
        self.history = []
        self.prompt = ''
        self.tasklist = [] # Needs to be initialized during show step 
                           # due to limitations on "context" knowledge
        self.writeoneach = True # Whether or not to write on each new task added
                                # TODO: Add to user settings

    def start(self, context):
        self.getTaskList(context, 'todo')
        if self.tasklist:
            self.history += [x.name for x in self.tasklist]

    def getTaskList(self, context, filename):
        self.tasklist = readTasks(context, filename)

    def writeTaskList(self, context, filename):
        writeTasks(self.tasklist, context, filename)

    def generateprompt(self):
        return "What are your tasks today?"

    def dostuff(self, userinput, context):
        self.tasklist.append(Task(userinput))
        if self.writeoneach:
            self.writeTaskList(context, 'todo')
    
    def cleanup(self, context):
        if not self.writeoneach:
            self.writeTaskList(context, 'todo')
