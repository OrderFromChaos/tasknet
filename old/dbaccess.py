from schclasses import Task, Todo # includes json, re, and datetime

todo = Todo()
todo.addTask(Task("Do Laundry"))
todo.addTask(Task("GTD Autoscheduler Draft",children=[Task('Turn tskdb.txt into a json file')]))
todo.writeToJson('data/todo.json')
print(todo)

# Now decompile
todo = Todo()
todo.readFromJson('data/todo.json')
print(todo)
