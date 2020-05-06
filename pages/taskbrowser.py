# needs to accept recursive todos
# display todo information on the side
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

from core.dbinterface import *
from collections import deque
from ordered_set import OrderedSet

import curses

class taskbrowser:
    def __init__(self, context):
        self.context = context
        self.tasks = self.getContent()
        
        # Cribbed from pages/common.numberSelectWithTitle
        curses.init_pair(500, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(500)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0

    def show(self, mainscreen):
        # make two windows;
        # left for name info,
        # right for metadata

        option_count = len(self.tasks)
        if option_count == 0:
            return {'url': 'mainmenu'}

        max_y, max_x = mainscreen.getmaxyx()
        rightbarsize = 40
        leftwindow = curses.newwin(max_y, max_x-rightbarsize, 0, 0)
        rightwindow = curses.newwin(max_y, rightbarsize, 0, max_x-rightbarsize)

        while True:
            ### 1. Left window #################################################

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
                    leftwindow.addstr(row, 2+depth, elt.name, self.hilite_color)
                else:
                    leftwindow.addstr(row, 2+depth, elt.name, self.normal_color)
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
            selkeys = {
                'name',
                'expected_length',
                'do by',
                'due date',
                'date added'
            }

            rightwindow.addstr(2, 2, f"Expected length: {selected.expectedlength}")
            if selected.duedate == None:
                rightwindow.addstr(3, 2, f"Do by: {selected.doby}")
            else:
                rightwindow.addstr(3, 2, f"Hard due date: {selected.duedate}", curses.COLOR_RED)
            rightwindow.addstr(4, 2, f"Date added: {selected.dateadded}")


            

            leftwindow.refresh()
            rightwindow.refresh()

            ### 3. Read keys ###################################################
            # Define key types
            down_keys = [curses.KEY_DOWN, ord('j')] # Hi vim users!
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]
            numbers = {ord(str(x)) for x in range(1, 10)}
            
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
                
            leftwindow.clear()
            rightwindow.clear()


                
            
        return {'url': 'mainmenu'}

    def getContent(self):
        return readTasks(self.context, 'todo')
