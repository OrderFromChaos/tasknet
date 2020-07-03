# Needs to be put into root directory to work properly

from core.dbinterface import *

res = readTasks('tasknet', 'todo')
print(res)