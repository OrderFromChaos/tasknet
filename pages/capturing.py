from core.dataclasses import *
from core.dbinterface import *
from pages.common import *
import re # Input validation

class capturing(inputWithScrollBack):
    def __init__(self, context):
        self.context = context
        self.prompt = ''

        self.writeoneach = True # Whether or not to write on each new task added
                                # TODO: Add to user settings
        self.tasklist = []
        self.getTaskList('todo')
        self.history = []
        if self.tasklist:
            self.history = [x.name for x in self.tasklist]

    def getTaskList(self, filename):
        self.tasklist = readTasks(self.context, filename)

    def writeTaskList(self, filename):
        writeTasks(self.tasklist, self.context, filename)

    def generateprompt(self):
        return "What are your tasks today?"

    def dostuff(self, userinput):
        self.tasklist.append(Task(userinput))
        # ^^ Will be appended to history on the next show step
        if self.writeoneach:
            self.writeTaskList('todo')
    
    def cleanup(self):
        if not self.writeoneach:
            self.writeTaskList('todo')
