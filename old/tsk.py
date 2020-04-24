import re # Used to check for typos in user input in the tsk() function
from datetime import datetime, now, timedelta # Used to keep track of times internally

### TODO: Allow for randomness when tasks have due dates (this decreases scheduling drift)
### TODO: Use a better task/project listing, the current structure is kinda stupid


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
        firstpass = True
        while True:
            if firstpass:
                response = input(string)
            else:
                response = input()
            if any([f(response) for f in expectations]):
                break
            else:
                print('Looks like you made a typo. Try again!')
                firstpass = False
        return response

    def dobyquestions(obj, todo, index, subindex = None): # Accepts either a Task or Project
        if type(obj) == Task:
            wording = 'task'
        elif type(obj) == Project:
            wording = 'project'
        response = tolerantinput('When would you like to complete the ' + wording + '''? Accepted inputs:
"datetime(2018,9,15)" which is YMD format
"quant + shortform time". For example, "3d", "2w". All accepted shortform times: [d, w]\n''',
[lambda x: re.compile(r"datetime\([0-9]{4},[0-9]{1,2},[0-9]{2}\)").findall(x)[0] == x, # I'm being very explicit here so as to catch all reasonable typos
 lambda x: re.compile("[0-9]+[dwm]").findall(x)[0] == x])

        timeofday = tolerantinput('Any particular time preferred for that day?\n"eod" for end of day\n"sod" for start of day\n"1847" a time in military format',
                          [lambda x: x == "eod" or x == "sod" or (x.isdigit() and len(x) == 4)])

        # The output from timeofday needs to be tolerantly fed into the final datetime() input eod rolls over to 00:00 of the next day sod is 00:00 of the current day for military time, 1847 is interpreted by strptime and then 
        # added to the other datetime object
        ### NOTE WHILE READING THIS: timedelta does not accept strings - it has to be an integer
        if timeofday == 'eod':
            timedel = timedelta(days=1)
        elif timeofday == 'sod':
            timedel = timedelta(days=0) # No change from expected date
        elif timeofday.isdigit():
            interpreted = datetime.strptime(response,'%H%M')
            timedel = timedelta(hours=interpreted.hour, minutes=interpreted.minute)

        if re.compile(r"datetime\([0-9]{4},[0-9]{1,2},[0-9]{2}\)").findall(response)[0] == response: # Datetime format
            if subindex:
                todo[index][subindex].doby = eval(response) + timedel # Fairly safe since regex
            else:
                todo[index].doby = eval(response) + timedel
        elif re.compile("[0-9]+[dw]").findall(response)[0] == response:
            nowtime = now() # Current date down to microseconds
            current_day = datetime(nowtime.year, nowtime.month, nowtime.day)
            # Add together the future date from the input and the expected hour of completion
            ### NOTE: timedelta does not accept strings - it has to be an integer
            if reponse[-1] == 'd':
                future = timedelta(days=int(response[:-1]))
            elif reponse[-1] == 'w':
                future = timedelta(days=7*int(response[:-1]))
            # This feature got removed because doing month adding in a user expected way is possibly non-solvable without significantly added input complexity.
            # elif response[-1] == 'm':
            #     future = timedelta(days=30*int(response[-1])) # TODO: This is not expected behavior on the part of the user.
                                                                # For example, someone might put down 1m on February 1st, expecting March 1st.
                                                                # Instead, they would get March 3rd.
            if subindex:
                todo[index][subindex].doby = current_day + future + timedel
            else:
                todo[index].doby = current_day + future + timedel
        return todo

    def taskquestions(task, todo, index, subindex=None):
        assert type(task) == Task, "taskquestions requires an input of class 'Task'"
        if task.exptime == None:
            print(task.name)
            response = tolerantinput('''What is the expected time to completion for this project in minutes?
Allowed options:
a number
"nc" if this is hard to assign a number to (hence needing further subtask work)
"p" if you want to pass on assigning an expected time right now\n''', [lambda x: x=="nc" or x=="p" or x.isdigit()])
            if response.isdigit(): # If the response is in minutes
                if subindex:
                    todo[index][subindex].exptime = int(response)
                else:
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
                    todo.append(Project(projtasks)) # TODO: For project inputs, this will current break out whatever subtask is part of the project, which loses some nesting hierarchy
                elif breakmethod == 'b':
                    print('Alrighty. Go ahead and name subtasks until you feel like you\'ve broken up the task fully. We\'ll add expected time later in the tsk cycle.')
                    print('When you\'re done, just input "exit".')
                    while True:
                        sometask = input()
                        if sometask == 'exit':
                            break
                        else:
                            todo.append(Task(sometask)) # TODO: Same hierarchy problem
            elif response == 'p':  # For completionist's sake
                pass
        if task.doby == None:
            todo = dobyquestions(task, todo, index, subindex=subindex)
        return todo

###################################################################################################################

    deletion_indices = [] # Probably not the safest way to do it (safest would be writing a new list),
                          # but this is a simple way to add the functionality of going back to the subtasks you just added.
    index = 0
    while index < len(todo): # List is dynamically changing
        event = todo[index]
        if type(event) == Task:
            todo = taskquestions(event, todo, index)
        elif type(event) == Project:
            # Projects have multiple todo events embedded, and also a general global todo date
            print('Working under project',event.name) # TODO: Add color highlighting for CLI
            if event.doby == None:
                todo = dobyquestions(event, todo, index) # Gets project due date
            # Now evaluate the subtasks
            print('Working under project',event.name)
            for subindex, subtask in enumerate(event.subtasks):
                todo = taskquestions(event, todo, index, subindex=subindex)
            TODO
            TODO
        else:
            raise NotImplementedError('Currently supported todo events are tasks and projects (essentially, folders for tasks)')
        index += 1

    while deletion_indices != []:
        del todo[deletion_indices[0]]
        del deletion_indices[0]
        deletion_indices = [x-1 for x in deletion_indices] # Shift over to the left
