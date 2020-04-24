import json
from typing import List
from core.dataclasses import *

# Needs to know the "context" it's writing in.
# This lets it select a folder in the style of data/<context>/todo.json
# or the like.

def writeTasks(L: List[Task], context: str, filename: str) -> None:
    L = [x.serialize() for x in L]
    prettyjson = json.dumps(L, indent=4)
    
    with open('data/' + context + '/' + filename + '.json', 'w') as f:
        f.write(prettyjson)

def readTasks(context, filename):
    with open('data/' + context + '/' + filename + '.json', 'r') as f:
        dataset = json.load(f)
    
    output = []
    for entry in dataset:
        t = Task()
        t.deserialize(entry)
        output.append(t)

    return output