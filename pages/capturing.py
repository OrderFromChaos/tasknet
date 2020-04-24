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
                                # TODO: Add to config
        self.prevstate = 0
        self.state = 0

    # def show(self, screen, context):

    #     self.getTaskList(context, 'todo')

    #     t = Task('Apply for a job',
    #              doby=datetime(2020, 4, 30)
    #              )

    #     self.tasklist.append(t)
        
    #     self.writeTaskList(context, 'todo')

    #     return {'url': 'mainmenu'}

    def show(self, mainscreen, context):
        # lines 2-3 are reserved for the current prompt and the text input box
        # lines 4-> are history (progresively greyed out)
        self.getTaskList(context, 'todo')
        if self.tasklist:
            self.history += [x.name for x in self.tasklist]

        contents = ''
        while contents not in {'exit ', 'q '}:
            prompt = self.generateprompt()
            
            mainscreen.clear()

            mainscreen.addstr(2, 2, prompt, curses.A_BOLD)
            # Render history
            for i, x in enumerate(self.history[-10:][::-1]):
                mainscreen.addstr(5+i, 4, x, curses.color_pair(247-i))

            mainscreen.refresh()
            textwindow = curses.newwin(1, mainscreen.getmaxyx()[1], 3, 4)
            box = textpad.Textbox(textwindow, True)
            contents = box.edit()
            del textwindow
            if contents not in {'exit ', 'q '}:
                self.history.append(contents)
                self.dostuff(contents, context)
        
        return {'url': self.exiturl()}

    def getTaskList(self, context, filename):
        self.tasklist = readTasks(context, filename)

    def writeTaskList(self, context, filename):
        writeTasks(self.tasklist, context, filename)
    
    def validate_input(userinput, method) -> str:
        # Accepts either a regex string or a function that returns a bool
        # Returns the validated string
        assert (isinstance(method, str) or callable(method))
        while True:
            if isinstance(method, str):
                regex = re.compile(method)
                if regex.findall(userinput)[0] == userinput:
                    return userinput
                else:
                    print('Looks like you made a typo. Try again!')
            else:
                if method(userinput):
                    return userinput
                else:
                    print('Looks like you made a typo. Try again!')

    def generateprompt(self):
        if self.state == 0:
            return "What are your tasks today?"

    def dostuff(self, userinput, context):
        if self.state == 0:
            self.tasklist.append(Task(userinput))
            if self.writeoneach:
                self.writeTaskList(context, 'todo')
