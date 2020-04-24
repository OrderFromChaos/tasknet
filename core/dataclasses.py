import json # Serialization for database
from datetime import datetime # Datetime class

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
        self.datefinished = None
    
    def __repr__(self):
        info = {
            'name': self.name,
            'expected length': self.expectedlength,
            'do by': self.doby,
            'due date': self.duedate,
            'children': self.children,
            'date added': self.dateadded,
            'date finished': self.datefinished
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
        if self.duedate:
            info['due date'] = self.duedate.strftime("%Y-%m-%d %H:%M:%S")
        if self.datefinished:
            info['date finished'] = self.datefinished.strftime("%Y-%m-%d %H:%M:%S")
        
        return info
    
    def deserialize(self, info: dict):
        assert isinstance(info, dict)
        assert set(info.keys()) == {
            'name',
            'expected length',
            'do by',
            'due date',
            'children',
            'date added',
            'date finished'
        }

        if info['expected length'] != None:
            assert isinstance(info['expected length'], int)
        if info['children']:
            for i, d in info['children']:
                t = Task()
                t.deserialize(d)
                info['children'][i] = t
        for k in ['do by', 'due date', 'date added', 'date finished']:
            if info[k]:
                info[k] = datetime.strptime(info[k], "%Y-%m-%d %H:%M:%S")
        
        self.name = info['name']
        self.expectedlength = info['expected length']
        self.doby = info['do by']
        self.duedate = info['due date']
        self.children = info['children']
        self.dateadded = info['date added']
        self.datefinished = info['date finished']


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