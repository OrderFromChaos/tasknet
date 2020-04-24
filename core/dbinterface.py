import json
import core.dataclasses as dataclasses

# Needs to know the "context" it's writing in.
# This lets it select a folder in the style of data/<context>/todo.json
# or the like.

def writeTasks(L: List[dataclasses.Task], context: str, filename: str) -> None:
    L = [x.serialize() for x in L]
    prettyjson = json.dumps(L, indent=4)
    
    with open('data/' + context + '/' + filename, 'w') as f:
        f.write(prettyjson)
