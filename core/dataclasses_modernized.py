import json
import pendulum
from dataclasses import dataclass, field
from weakref import finalize
from pathlib import Path

class UUIDGenerator:

    def __init__(self):
        # Open UUID file
        self.f = open(Path(__file__).absolute().parent.parent / 'data/persistent_test.json', 'r+')
        self.data = json.load(self.f)
        finalize(self, self.cleanup)

    def generate(self):
        curr = self.data['curr_uuid']
        self.data['curr_uuid'] += 1
        return curr

    def cleanup(self):
        print('Writing, closing file, and exiting UUIDGenerator')
        self.f.seek(0)
        json.dump(self.data, self.f, indent=4)
        self.f.truncate()
        self.f.close()


@dataclass
class Task:
    context: str
    name: str
    uuid: int
    children: list = field(default_factory=list)
    length: int = -1
    due_date: pendulum.datetime = None
    do_by: pendulum.datetime = None
    gen_date: pendulum.datetime = pendulum.now()
    finish_date: pendulum.datetime = None


if __name__ == '__main__':
    t = Task(
        'tasknet',
        'allow for "a" insertion at end of list',
        5315
    )
    print(t)

    c = UUIDGenerator()
    uuid = c.generate()
