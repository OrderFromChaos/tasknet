import json # Serialization for database
from datetime import datetime # Datetime class

class Task:
    def __init__(self, context, name='', expectedlength=None, doby=None, duedate=None, children=[], uid=None, rootbool=True):
        # do by = soft deadline, autoscheduler will try and keep it
        # due date = hard deadline, autoscheduler will return an error if it
        #            cannot be finished

        if context == 'lostnfound':
            raise Exception('Task improperly formed by a page; contact developer (sourceforgery@gmail.com) with traceback.')

        # Strict construction checks
        assert isinstance(name, str)
        if expectedlength:
            assert isinstance(expected_length, int)
        if doby:
            assert isinstance(doby, datetime)
        if duedate:
            assert isinstance(duedate, datetime)
        if children:
            for c in children:
                assert isinstance(c, Task)

        ### Member variables
        if uid != None:
            # Assume external functions handle updating meta.json appropriately
            self.uid = int(uid)
        else:
            # Inefficent! Try and avoid
            with open('data/meta.json', 'r') as f:
                db = json.load(f)
            self.uid = db['curr_uid']
            db['curr_uid'] += 1
            with open('data/meta.json', 'w') as f:
                json.dump(db, f, indent=4)
        self.name = name
        self.expectedlength = expectedlength
        self.doby = doby
        self.duedate = duedate
        self.children = [int(x) for x in children]
        self.dateadded = datetime.now()
        self.datefinished = None
        self.rootbool = rootbool
        self.context = context
        self.leaftag = False

    def __repr__(self):
        info = {
            'uid': self.uid,
            'name': self.name,
            'expected length': self.expectedlength,
            'do by': self.doby,
            'due date': self.duedate,
            'date added': self.dateadded,
            'date finished': self.datefinished,
            'children': self.children,
            'rootbool': self.rootbool,
            'context': self.context,
            'leaftag': self.leaftag
        }
        return str(info)
    
    def serialize(self):
        # Prep for database input
        info = {'name': self.name,
                'expected length': self.expectedlength,
                'do by': None,
                'due date': None,
                'date added': self.dateadded.strftime("%Y-%m-%d %H:%M:%S"),
                'date finished': None,
                'children': self.children,
                'rootbool': self.rootbool,
                'leaftag': self.leaftag
                }
        
        if self.doby:
            info['do by'] = self.doby.strftime("%Y-%m-%d %H:%M:%S")
        if self.duedate:
            info['due date'] = self.duedate.strftime("%Y-%m-%d %H:%M:%S")
        if self.datefinished:
            info['date finished'] = self.datefinished.strftime("%Y-%m-%d %H:%M:%S")
        
        return info
    
    def deserialize(self, entry: dict, uid: int):
        # context is already determined during initialization, so no need to pass into entry dict
        assert isinstance(entry, dict)
        minimal_keys = {
            'name',
            'expected length',
            'do by',
            'due date',
            'children',
            'date added',
            'date finished',
            'rootbool'
        }
        assert (set(entry.keys()) & (minimal_keys)) == minimal_keys

        if entry['expected length'] != None:
            assert isinstance(entry['expected length'], int)
        for k in ['do by', 'due date', 'date added', 'date finished']:
            if entry[k]:
                entry[k] = datetime.strptime(entry[k], "%Y-%m-%d %H:%M:%S")
        
        self.name =            entry['name']
        self.expectedlength =  entry['expected length']
        self.doby =            entry['do by']
        self.duedate =         entry['due date']
        self.children =        entry['children']
        self.dateadded =       entry['date added']
        self.datefinished =    entry['date finished']
        self.rootbool =        entry['rootbool']
        if 'leaftag' in entry:
            self.leaftag =     entry['leaftag']
        else:
            self.leaftag =     False
        self.uid =             uid