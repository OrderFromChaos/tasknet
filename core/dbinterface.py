import json
from core.dataclasses import *
from collections import OrderedDict

# Needs to know the "context" it's writing in.
# This lets it select a folder in the style of data/<context>/todo.json
# or the like.

def writeTasks(taskdict, context, filename, overwrite=True):
    if overwrite == False:
        with open(f'data/{context}/{filename}.json', 'r') as f:
            taskdict = OrderedDict(x.items() for x in json.load(f, object_pairs_hook=OrderedDict))
    if taskdict:
        olddict = OrderedDict([(x, y.serialize()) for x, y in taskdict.items()])
    else:
        olddict = OrderedDict()

    if overwrite == False:
        taskdict.update(olddict)
    else:
        taskdict = olddict

    prettyjson = json.dumps(taskdict, indent=4)
    with open(f'data/{context}/{filename}.json', 'w') as f:
        f.write(prettyjson)

def readTasks(context, filename):
    # Output format:
    # {
    #     '3': Task,
    #     ...
    # }
    with open('data/' + context + '/' + filename + '.json', 'r') as f:
        dataset = json.load(f, object_pairs_hook=OrderedDict)
    
    output = OrderedDict()
    for uid in dataset:
        entry = dataset[uid]
        t = Task(context, uid=-1) # To avoid automated UID incrementing
        t.deserialize(entry, uid)
        output[int(uid)] = t

    return output