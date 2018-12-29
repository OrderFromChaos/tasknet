import json

class Task:
    def __init__(self, name, expected_length=None, doby=None, duedate=None, children=[]):
        # Everything except name is set to None by default for external imports
        assert type(name) == str
        self.name = name
        self.exptime = expected_length
        self.doby = doby
        self.children = children
    def __repr__(self):
        return str((self.name,self.exptime,self.doby,self.children))
    def __dict__(self):
        # For json serialization
        return {"name":self.name,
                "exptime":str(self.exptime), # Expected to be either None or datetime obj.
                "doby":str(self.doby),
                "children":[x.__dict__() for x in self.children]
                }

todo = [Task("Do Laundry"),
        Task("GTD Autoscheduler Draft",children=[Task('Turn tskdb.txt into a json file')])
]

targetfile = 'tskdb.txt'
prettyjson = json.dumps([x.__dict__() for x in todo],indent=4)
with open(targetfile,'w') as f:
    f.write(prettyjson)
