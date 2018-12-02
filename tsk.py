import re # Used to check for typos in user input in the tsk() function

class Task:
    def __init__(self, name, expected_length=None, doby=None, duedate=None):
        # Everything except name is set to None by default for external imports
        assert type(name) == str
        self.name = name
        self.exptime = expected_length
        self.doby = doby
    def __repr__(self):
        # For dev checkups
        return 'task(name="' + self.name + '", exptime=' + str(self.exptime) + ', doby=' + str(self.doby) + ', due=' + str(self.due) + ')'

class Project:
    def __init__(self, subtasks, doby=None):
        assert type(subtasks[0]) == Task, "Subtask input should be instances of class 'task'"
        self.subtasks = subtasks
        self.doby = doby

todo = [Task('GTD Autoscheduler Draft'),
        Task('Do laundry', expected_length=20, doby='today')]

# for subtask in todo:
#     print(subtask)

def tsk():
    # Find all tasks that need clarification.
    # 1. Get all tasks that don't currently have an expected length or duedate
    # 2. Find all projects that don't currently have a duedate
    # 3. Carefully pay attention to if project subtasks are being given a later duedate than the project itself

    def tolerantinput(string, expectations):
        # Expectations are a list of functions which return True if the string is in the expected format.
        # If not, it'll say you made a typo and ask again.
        while True:
            response = input(string)
            if any([f(response) for f in expectations]):
                break
            else:
                print('Looks like you made a typo. Try again!')
        return response

    def taskquestions(task, todo):
        assert type(task) == Task, "taskquestions requires an input of class 'Task'"
        if task.exptime == None:
            print(task.name)
            response = tolerantinput('''What is the expected time to completion for this project in minutes?
Allowed options:
a number
"nc" if this is hard to assign a number to (hence needing further subtask work)
"p" if you want to pass on assigning an expected time right now
''', [lambda x: x=="nc" or x=="p", lambda x: x.isdigit()])
            if response.isdigit(): # If the response is in minutes
                todo[index].exptime = int(response)
            elif response == 'nc': # Needs to be broken into subtasks
                breakmethod = tolerantinput('Would you like to break up the current task: ' + task.name + '\n"a" by turning it into a project with subtasks\n or "b" by replacing it with a number of smaller tasks?',
                                            [lambda x: x == "a" or x == "b"])
                deletion_indices.append(index) # Either way the subtask is getting removed at the end
                if breakmethod == 'a':
                    print('Alrighty. Go ahead and name subtasks until you feel like you accounted for the project needs. We\'ll add expected time later in the tsk cycle.')
                    print('When you\'re done, just input "exit".')
                    projtasks = []
                    while True:
                        sometask = input()
                        if sometask == 'exit':
                            break
                        else:
                            projtasks.append(Task(sometask))
                    todo.append(Project(projtasks))
                elif breakmethod == 'b':
                    TODO
            elif response == 'p':  # For completionist's sake
                pass
        if task.doby == None:
            response = tolerantinput('''When would you like to complete the task? Accepted inputs:
"datetime(2018,9,15)" which is YMD format
"quant + shortform time". For example, "3d", "2w". All accepted shortform times: [d, w, m]
''',
[lambda x: re.compile(r"datetime\([0-9]{4},[0-9]{1,2},[0-9]{2}\)").findall(x)[0] == x, # I'm being very explicit here so as to catch all reasonable typos
 lambda x: re.compile("[0-9]+[dwm]").findall(x)[0] == x])
        return todo

###################################################################################################################

    deletion_indices = [] # Probably not the safest way to do it (safest would be writing a new list),
                          # but this is a simple way to add the functionality of going back to the subtasks you just added.
    index = 0
    while index < len(todo): # List is dynamically changing
        event = todo[index]
        if type(event) == Task:
            todo = taskquestions(event, todo)
        elif type(event) == Project:
            TODO
            TODO
        else:
            raise NotImplementedError('Currently supported todo events are tasks and projects (essentially, folders for tasks)')
        index += 1

    while deletion_indices != []:
        del todo[deletion_indices[0]]
        deletion_indices = [x-1 for x in deletion_indices] # Shift over to the left
