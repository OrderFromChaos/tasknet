import json
import re # Confirming that input is okay from json file
import datetime # Decompiling json

class Task:
    def __init__(self, name, expected_length=None, doby=None, duedate=None, children=[]):
        # Everything except name is set to None by default for external imports
        self.name = name
        self.exptime = expected_length
        self.doby = doby
        self.children = children # List of Task objects
    def __repr__(self):
        return str((self.name,self.exptime,self.doby,self.children))

    def __dict__(self,finishdate=False):
        # For json serialization
        if finishdate: # Adds current date so you know when you finished the task
            return {"name":self.name,
                    "exptime":str(self.exptime), # Expected to be either None or datetime obj.
                    "doby":str(self.doby),
                    "children":[x.__dict__() for x in self.children],
                    "finishdate":datetime.datetime.now()
                    }
        else:
            return {"name":self.name,
                    "exptime":str(self.exptime), # Expected to be either None or datetime obj.
                    "doby":str(self.doby),
                    "children":[x.__dict__() for x in self.children]
                    }

class Todo:
    def __init__(self, subtasks=[]):
        self.subtasks = []
    def __repr__(self):
        return str(self.subtasks)
    def addTask(self, taskobj):
        self.subtasks.append(taskobj)

    # Json interaction functions
    def writeToJson(self,filename):
        prettyjson = json.dumps([x.__dict__() for x in self.subtasks],indent=4)
        with open(filename,'w') as f:
            f.write(prettyjson)
    def readFromJson(self,filename):
        with open(filename, 'r') as f:
            dataset = json.load(f)

        # Disallow badly formed json files using re
        def deconvJson(jsontask):
            # task name is straightforward to reconstruct

            # exptime is either None or a number
            raw_exptime = jsontask['exptime']
            if raw_exptime == 'None':
                exptime = None
            else:
                nummatch = re.compile("[0-9\.]+")
                if nummatch.findall(raw_exptime) == raw_exptime:
                    exptime = eval(raw_exptime)
                else:
                    raise Exception('Invalid json string for exptime',raw_exptime)

            # doby is either None or a datetime obj
            raw_doby = jsontask['doby']
            if raw_doby == 'None':
                doby = None
            else:
                datetimematch = "datetime\([0-9]{4},[0-9]{1,2},[0-9]{1,2}\)"
                if datetimematch.findall(raw_doby) == raw_doby: # BUG: Will probably be datetime.datetime in print
                    doby = eval(raw_doby)
                else:
                    raise Exception('Invalid json string for doby',raw_doby)

            # Children can be defined recursively
            return Task(name=jsontask['name'],expected_length=exptime,doby=doby,children=[deconvJson(x) for x in jsontask['children']])

        self.subtasks = [deconvJson(subtask) for subtask in dataset]
