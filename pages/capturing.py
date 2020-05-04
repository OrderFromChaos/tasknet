from core.dataclasses import *
from core.dbinterface import *
from pages.common import *
import re # Input validation

class capturing(inputWithScrollBack):
    def __init__(self, context):
        # TODO: Rewrite this to not read from memory each time like a dum dum

        self.history = []
        self.prompt = ''
        self.tasklist = [] # Needs to be initialized during show step 
                           # due to limitations on "context" knowledge
        self.writeoneach = True # Whether or not to write on each new task added
                                # TODO: Add to user settings
        self.context = context

    def start(self):
        self.getTaskList('todo')
        if self.tasklist:
            self.history += [x.name for x in self.tasklist]

    def getTaskList(self, filename):
        self.tasklist = readTasks(self.context, filename)

    def writeTaskList(self, filename):
        writeTasks(self.tasklist, self.context, filename)

    def generateprompt(self):
        return "What are your tasks today?"

    def dostuff(self, userinput):
        self.tasklist.append(Task(userinput))
        if self.writeoneach:
            self.writeTaskList('todo')
    
    def cleanup(self):
        if not self.writeoneach:
            self.writeTaskList('todo')
