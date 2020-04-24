import json
import re # Confirming that input is okay from json file
import datetime # Decompiling json

class Task:
    def __init__(self, name, expected_length=None, doby=None, dateadd=None, children=[]):
        # Everything except name is set to None by default for external imports
        self.name = name
        self.exptime = expected_length
        self.doby = doby
        self.dateadd = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.children = children # List of Task objects
    def __repr__(self):
        return str((self.name,self.exptime,self.doby,self.dateadd,self.children))
    def __dict__(self,finishdate=False):
        # For json serialization
        basedict = {"name":self.name,
                    "exptime":str(self.exptime), # Expected to be either None or datetime obj.
                    "doby":str(self.doby),
                    "dateadd":str(self.dateadd),
                    "children":[x.__dict__() for x in self.children]
                    }
        if finishdate: # Adds current date so you know when you finished the task
            basedict["finishdate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return basedict

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
                if nummatch.findall(raw_exptime)[0] == raw_exptime:
                    exptime = eval(raw_exptime)
                else:
                    raise RuntimeError('Invalid json string for exptime',raw_exptime)


            # doby is either None or a datetime obj
            raw_doby = jsontask['doby']
            datetimematch = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}")
            if raw_doby == 'None':
                doby = None
            else:
                if datetimematch.findall(raw_doby)[0] == raw_doby: # BUG: Will probably be datetime.datetime in print
                    doby = raw_doby
                else:
                    raise RuntimeError('Invalid json string for doby',raw_doby)
            
            # dateadded is the same thing
            raw_dateadd = jsontask['dateadd']
            if datetimematch.findall(raw_dateadd)[0] == raw_dateadd:
                dateadd = raw_dateadd
            else:
                print(datetimematch.findall(raw_dateadd))
                raise RuntimeError('Invalid json string for initial date',raw_dateadd)

            # Children can be defined recursively
            return Task(name=jsontask['name'],expected_length=exptime,doby=doby,dateadd=dateadd,children=[deconvJson(x) for x in jsontask['children']])

        self.subtasks = [deconvJson(subtask) for subtask in dataset]
