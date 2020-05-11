# needs to accept recursive todos
# display todo information on the side
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

from core.dbinterface import *
from collections import deque
from ordered_set import OrderedSet

import curses
from datetime import timedelta
from copy import deepcopy

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
            ### 1. Left window #################################################
            leftwindow.border()

            # Observation: the first element of todo.json is
            #       always guaranteed to be a top level task
            todisplay = OrderedSet(self.tasks.keys())
            d = deque()
            d.append((todisplay[0], 0))

            row = 2
            counter = 0
            while todisplay:
                if d:
                    curr, depth = d.popleft()
                else:
                    curr, depth = todisplay[0], 0
                todisplay.remove(curr)
                elt = self.tasks[curr]

                if counter == self.selected_option:
                    seluid = curr # Used for later steps
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
                    for i in elt.children:
                        d.append((i, depth+1))
                
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

            def naturaldate(truedate):
                # Possible outputs:
                # Jan 21, 2052 (if 11:59pm and date is not current year)
                # Jan 21 (if 11:59pm and date is this year)
                # Thursday (if the date is this week and 11:59pm)
                # next Thursday (if date is next week and 11:59pm)
                # X 10:00am (if the due date is not 11:59 on the previous options)
                # TODO: Allow additional fuzziness (like "a month from now" or something)
                #       in config
                output = []
                now = datetime.now()
                # Assuming day of the week starts on Sunday
                nowmorn = datetime(now.year, now.month, now.day)
                floorweek = nowmorn - timedelta(days=(nowmorn.weekday()+1) % 7)
                ceilweek = floorweek + timedelta(days=6, hours=23, minutes=59)
                lastweek = floorweek - timedelta(days=7)
                nextweek = ceilweek + timedelta(days=7)

                if lastweek <= truedate < floorweek:
                    output.append('last')
                    output.append(truedate.strftime(r'%A'))
                elif floorweek <= truedate <= ceilweek:
                    output.append(truedate.strftime(r'%A'))
                elif ceilweek < truedate <= nextweek:
                    output.append('next')
                    output.append(truedate.strftime(r'%A'))
                else:
                    output.append(truedate.strftime(r'%b %d'))
                    if now.year != truedate.year:
                        output.append(truedate.strftime(r'%Y'))

                if truedate.strftime(r'%I:%M%p') != '11:59PM':
                    output.append(truedate.strftime(r'%I:%M%p'))

                return ' '.join(output)

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
            
            userinput = mainscreen.getch()
            if userinput == ord('q'):
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
            elif userinput == curses.KEY_RESIZE:
                max_y, max_x = mainscreen.getmaxyx()

                leftwindow.resize(max_y, max_x-rightbarsize)
                rightwindow.mvwin(0, max_x-rightbarsize)


                # TODO: Can't get it to redraw properly for some reason...

                # leftwindow.clear()
                # rightwindow.clear()

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
            elif userinput in add_keys:
                # Create a new task
                # TODO: Make this as efficient as capturing
                #       ie; append vs. open file
                # Need to have the input somewhere;
                #    probably try and put it in-place of where it's going?
                pass

                
            leftwindow.clear()
            rightwindow.clear()
        
        del leftwindow, rightwindow

        if self.tasksmodified:
            # 1. Write finished tasks
            # 2. Filter finished tasks from self.tasks
            # 3. Rewrite filtered self.tasks to todo.json
            writeTasks(self.fintasks, self.context, 'finished')

            nfinroots = [x for x,y in self.tasks.items() 
                                        if y.rootbool == True
                                        and y.datefinished == None]
            
            # Nested gathering of all child UIDs
            stack = nfinroots
            all_uids = []
            while stack:
                top = stack.pop()
                elt = self.tasks[top]
                all_uids.append(top)
                if elt.children:
                    stack.extend(elt.children)

            all_uids.sort() # Data file should always store UIDs in order

            filtered = {x: self.tasks[x] for x in all_uids}
            
            writeTasks(filtered, self.context, 'todo')

        return {'url': 'mainmenu'}

    def getContent(self):
        return readTasks(self.context, 'todo')
