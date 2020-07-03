# TODO:
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

# Repo-internal libraries
from core.dbinterface import *                  # Reading and writing tasks
from core.utility import naturaldate            # Making datetimes nice and readable 
from core.customtextbox import CustomTextbox    # Backspace-supported editing

# Standard libraries
import curses                       # Primary renderer
from collections import deque       # BFS
from copy import deepcopy           # List deepcopy for DFS iteration

# External dependencies
from ordered_set import OrderedSet  # Surprisingly not a part of python stdlib

DEBUG = True # TODO: Make this a main passed SETTINGS dict later on

class taskbrowser:
    def __init__(self, context):
        self.context = context
        self.tasks = self.getContent()
        self.fintasks = dict()
        
        # Cribbed from pages/common.numberSelectWithTitle
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0
        self.tasksmodified = False

        self.passthrough = False
        self.addtask = None

    def show(self, mainscreen):
        # make two windows;
        # left for name info,
        # right for metadata
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        option_count = len(self.tasks)
        if option_count == 0:
            return {'url': 'mainmenu'}

        max_y, max_x = mainscreen.getmaxyx()
        rightbarsize = 40
        leftwindow = curses.newwin(max_y, max_x-rightbarsize, 0, 0)
        rightwindow = curses.newwin(max_y, rightbarsize, 0, max_x-rightbarsize)

        while True:
            option_count = len(self.tasks)
            
            # mainscreen.addstr(max_y-3, max_x-5, "{:3}".format(self.selected_option))

            ### 1. Left window #################################################
            leftwindow.border()

            # Append a root task to start with
            todisplay = OrderedSet(self.tasks.keys())
            d = []
            for k in todisplay:
                elt = self.tasks[k]
                if elt.rootbool:
                    d.append((k, 0))
                    break

            row = 2
            counter = 0
            while todisplay:
                if d:
                    curr, depth = d.pop()
                else:
                    curr, depth = todisplay[0], 0
                todisplay.remove(curr)
                elt = self.tasks[curr]

                if self.passthrough:
                    if elt.name == '`~12~~':
                        selrow = row
                        selcol = depth+2

                if counter == self.selected_option:
                    seluid = curr # Used for later steps
                    selrow = row
                    selcol = depth+2
                    
                    if elt.datefinished == None:
                        leftwindow.addstr(row, 2+depth, elt.name, self.hilite_color)
                    else:
                        leftwindow.addstr(row, 2+depth, elt.name, curses.color_pair(2))
                else:
                    if elt.datefinished == None:
                        leftwindow.addstr(row, 2+depth, elt.name, self.normal_color)
                    else:
                        leftwindow.addstr(row, 2+depth, elt.name, curses.color_pair(3))
                row += 1
                counter += 1
                if elt.children:
                    for i in reversed(elt.children):
                        d.append((int(i), depth+2))
                
                if row >= max_y: # Don't try and display the too-long rows
                    break
            
            # TODO: Implement a scrolling system for both:
            # 1. Too-nested tasks (scroll to right)
            # 2. Too many tasks (scroll down)
            # Also, pgup and pgdown support for first and last tasks
            # Maybe a special button for browsing top-level tasks

            ### 2. Right window ################################################
            rightwindow.border()

            selected = self.tasks[list(self.tasks.keys())[self.selected_option]]

            rightwindow.addstr(2, 2, f"Expected length: {selected.expectedlength}")
            if selected.duedate == None:
                out = selected.doby
                if out:
                    out = naturaldate(out)
                rightwindow.addstr(3, 2, f"Do by: {out}")
            else:
                out = selected.duedate
                if out:
                    out = naturaldate(out)
                rightwindow.addstr(3, 2, f"Hard due date: {out}", curses.COLOR_RED)
            rightwindow.addstr(4, 2, f"Date added: {naturaldate(selected.dateadded)}")

            leftwindow.refresh()
            rightwindow.refresh()

            ### 3. Read keys ###################################################
            # Define key types
            down_keys = [curses.KEY_DOWN, ord('j')] # Hi vim users!
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]
            numbers = {ord(str(x)) for x in range(1, 10)}
            done_keys = [ord('d')]
            add_keys = [ord('a')]
            edit_keys = [ord('e')]
            meta_keys = [ord('m')]
            
            if self.passthrough:
                userinput = ord('a')
            else:
                userinput = mainscreen.getch()
            
            if DEBUG:
                if 31 < userinput < 126:
                    mainscreen.addstr(max_y-3, max_x-3, chr(userinput))

            if userinput in exit_keys:
                break
            elif userinput in down_keys:
                if self.selected_option < option_count - 1:
                    self.selected_option += 1
                else:
                    self.selected_option = 0 # Wraparound
            elif userinput in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count - 1
            elif userinput in edit_keys:
                # Overwrite the current position of the option
                textwindow = curses.newwin(1, max_x-rightbarsize-1-selcol, selrow, selcol)
                box = CustomTextbox(textwindow, border=False, contents=selected.name)
                # curses.doupdate()
                contents = box.edit()
                del textwindow

                # Overwrite name in memory
                self.tasks[list(self.tasks.keys())[self.selected_option]].name = contents # TODO: Is this really the minimal edit call?
                self.tasksmodified = True
            elif userinput == curses.KEY_RESIZE:
                max_y, max_x = mainscreen.getmaxyx()

                leftwindow.resize(max_y, max_x-rightbarsize)
                rightwindow.mvwin(0, max_x-rightbarsize)


                # TODO: Can't get it to redraw properly for some reason...

                # leftwindow.clear()
                # rightwindow.clear()
                
                # curses.doupdate()

                # leftwindow.noutrefresh()
                # rightwindow.noutrefresh()

                # curses.doupdate()
            elif userinput in done_keys:
                # Mark a task as "complete"
                # 1. If nested, mark but don't move
                # 2. If top level, mark and move to finished.json

                # Mark task using seluid from draw step
                self.tasks[seluid].datefinished = datetime.now()

                elt = self.tasks[seluid]
                if elt.rootbool:
                    # Add to self.fintasks (and all the children!)
                    # Note that children maintain whatever finished state
                    #   they originally had, so this can be used in the
                    #   future for any prompts like "did you finish this subtask?"
                    #   if that task.datefinished == None.
                    self.fintasks[seluid] = elt
                    stack = deepcopy(elt.children)
                    while stack:
                        top = stack.pop()
                        elt = self.tasks[top]
                        self.fintasks[top] = elt

                        if elt.children:
                            stack.extend(elt.children)

                self.tasksmodified = True
                # TODO: Add perma-delete - if d is pressed twice
            elif userinput in add_keys:
                # Create a new task
                # TODO: Make this as efficient as capturing
                #       ie; append vs. open file
                # 1. Add a dummy blank task to the task list as a child
                #    of the intended parent
                # 2. Loop through the draw step again, with self.passthrough
                #    set to true
                # 3. Overwrite the self.passthrough row with an editbox
                # 4. Overwrite the dummy task with the actual input task
                # 5. Set self.tasksmodified to True
                if not self.passthrough:
                    t = Task(name='`~12~~', rootbool=False) # Properly populates UID (though inefficiently)
                    self.tasks[t.uid] = t
                    self.addtask = t

                    self.tasks[seluid].children.append(t.uid)
                    self.passthrough = True
                else:
                    textwindow = curses.newwin(1,
                                               max_x-selcol-rightbarsize-1, 
                                               selrow,
                                               selcol
                                               )
                    box = CustomTextbox(textwindow)
                    contents = box.edit()
                    del textwindow

                    self.tasks[self.addtask.uid].name = contents

                    self.passthrough = False
                    self.tasksmodified = True
            elif userinput in meta_keys:
                with open('data/meta.json', 'r') as f:
                    metasettings = json.load(f)
                
                # if 'metacontexts' not in metasettings:
                #     metacontexts = getMetaContexts()
                #     metasettings['metacontexts'] = metacontexts
                #     with open('data/meta.json', 'r') as f:
                #         json.dump(metasettings, f)
                # else:
                #     metacontexts = metasettings['metacontexts']
                metacontexts = ['household', 'career']

                # Add all tasks from each context to the taskbrowser list
                # For each task, add a tag with the context source
                # While rendering, prepend with a (context) name

                # Allow for editing/writing similar to single-context view

                # TODO Step 1: Rewrite task file writing method to make this trivial
                #   (just pass in a list of tasks and a context to write to)
                #   (then just use list comprehensions and calls to the new fxn)
                # TODO Step 2ish: Figure out why the passthrough task is necessary
                #   (if it is, standardize the name)

            leftwindow.clear()
            rightwindow.clear()

        del leftwindow, rightwindow

        if self.tasksmodified:
            # 1. Write finished tasks
            # 2. Filter finished tasks from self.tasks
            # 3. Rewrite filtered self.tasks to todo.json
            if self.fintasks:
                writeTasks(self.fintasks, self.context, 'finished')

            nfinroots = [x for x,y in self.tasks.items() 
                                        if y.rootbool == True
                                        and y.datefinished == None]
            
            # Nested gathering of all child UIDs
            queue = deque(nfinroots)
            all_uids = []
            while queue:
                top = queue.popleft()
                elt = self.tasks[top]
                all_uids.append(top)
                if elt.children:
                    queue.extend(elt.children)

            filtered = OrderedDict([(x, self.tasks[x]) for x in all_uids])
            
            writeTasks(filtered, self.context, 'todo')

        return {'url': 'mainmenu'}

    def getContent(self):
        return readTasks(self.context, 'todo')
