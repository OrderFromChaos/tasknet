import json
from datetime import datetime

class Task:
    def __init__(self, name, expected_length=None, doby=None, duedate=None, children=[]):
        # do by = soft deadline, autoscheduler will try and keep it
        # due date = hard deadline, autoscheduler will return an error if it
        #            cannot be finished

        # Strict construction checks
        assert isinstance(name, str)
        if expected_length:
            assert isinstance(expected_length, int)
        if doby:
            assert isinstance(doby, datetime)
        if duedate:
            assert isinstance(duedate, datetime)
        if children:
            for c in children:
                assert isinstance(c, Task)

        # Member variables
        self.name = name
        self.expectedlength = expectedlength
        self.doby = doby
        self.duedate = duedate
        self.children = children
        self.dateadded = datetime.now()
    
    def __repr__(self):
        info = {
            'name': self.name,
            'expected length': self.expectedlength,
            'do by': self.doby
            'due date': self.duedate
        }
        return str(info)
    
    def serialize(self):
        # Prep for database input
        info = {'name': self.name,
                'expected length': self.expectedlength,
                'date added': self.dateadded.strftime("%Y-%m-%d %H:%M:%S")
                'children': self.children}
        
        if self.doby:
            info['do by'] = self.doby.strftime("%Y-%m-%d %H:%M:%S")
        else:
            info['do by'] = None
        
        if self.duedate:
            info['due date'] = self.duedate.strftime("%Y-%m-%d %H:%M:%S")
        else:
            info['due date'] = None
        
        return info


# class Project:
#     # Just a folder for Tasks
#     def __init__(self, subtasks, doby=None, duedate=None):
#         if subtasks:
#             assert isinstance(subtasks[0], Task), "Subtask input should be instances of class 'Task'"

#         self.subtasks = subtasks
#         self.doby = doby
#         self.duedate = duedate
    
#     def add(self, subtask: Task):
#         if not isinstance(subtask, Task):
#             raise Exception('Attempt to add non-Task to Project:\n'
#                             str(subtask))
#         else:
#             self.subtasks.append(subtask)