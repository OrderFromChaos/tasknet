# Standard libraries
import json
import logging
from dataclasses import dataclass, field # core dataclass lib
from pathlib import Path
from weakref import finalize # guaranteed cleanup on garbage collection

# Pypi libraries
import pendulum

class UUIDGenerator:
    """
    Keeps a persistent UUID open the whole program runtime and writes to file when garbage collected.
    During program flow, this will be stored in the PageHandler, so it will be GC at the same time as program exit.
    """

    def __init__(self):
        # Open UUID file
        self.uuidpath = Path(__file__).absolute().parent.parent / 'data/persistent_test.json'
        with open(self.uuidpath, 'r') as f:
            self.data = json.load(f)
        finalize(self, self.cleanup)

    def generate(self):
        curr = self.data['curr_uuid']
        self.data['curr_uuid'] += 1
        return curr

    def cleanup(self):
        logging.debug(f'Writing new max UUID: {self.data["curr_uuid"]}')
        with open(self.uuidpath, 'w') as f:
            json.dump(self.data, f, indent=4)


@dataclass
class Task:
    context: str
    name: str
    uuid: int # Expected that upstream calls UUIDGenerator.generate()
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
    print(uuid)