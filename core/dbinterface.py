import json
from typing import List
from core.dataclasses import *

# Needs to know the "context" it's writing in.
# This lets it select a folder in the style of data/<context>/todo.json
# or the like.

def writeTasks(taskdict, context: str, filename: str) -> None:
    taskdict = {x: y.serialize() for x, y in taskdict.items()}
    prettyjson = json.dumps(taskdict, indent=4)
    
    with open('data/' + context + '/' + filename + '.json', 'w') as f:
        f.write(prettyjson)

def readTasks(context, filename):
    # Output format:
    # {
    #     '3': Task,
    #     ...
    # }
    with open('data/' + context + '/' + filename + '.json', 'r') as f:
        dataset = json.load(f)
    
    output = dict()
    for uid in dataset:
        entry = dataset[uid]
        t = Task(uid=-1) # To avoid automated UID incrementing
        t.deserialize(entry, uid)
        output[int(uid)] = t

    return output