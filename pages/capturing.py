from core.dataclasses import *
from core.dbinterface import *
from pages.common import *

class capturing(inputWithScrollBack):
    def __init__(self, context):
        self.context = context
        self.prompt = ''

        self.writeoneach = True  # Whether or not to write on each new task added
                                 # TODO: Add to user settings
        self.tasklist = dict()
        self.getTaskList('todo')
        self.history = []
        if self.tasklist:
            self.history = [self.tasklist[x].name for x in self.tasklist]

        with open('data/meta.json', 'r') as f:
            db = json.load(f)
        self.curr_uid = db['curr_uid'] 

    def getTaskList(self, filename):
        self.tasklist = readTasks(self.context, filename)

    def writeTaskList(self, filename):
        writeTasks(self.tasklist, self.context, filename)

    def generateprompt(self):
        return "What are your tasks today?"

    def dostuff(self, userinput):
        self.tasklist[self.curr_uid] = Task(userinput, uid=self.curr_uid)
        self.curr_uid += 1
        # ^^ Will be appended to screen history on the next show step
        if self.writeoneach:
            self.writeTaskList('todo')
            with open('data/meta.json', 'r') as f:
                db = json.load(f)
            db['curr_uid'] = self.curr_uid
            with open('data/meta.json', 'w') as f:
                json.dump(db, f, indent=4)
    
    def cleanup(self):
        if not self.writeoneach:
            self.writeTaskList('todo')
            with open('data/meta.json', 'r') as f:
                db = json.load(f)
            db['curr_uid'] = self.curr_uid
            with open('data/meta.json', 'w') as f:
                json.dump(db, f, indent=4)
