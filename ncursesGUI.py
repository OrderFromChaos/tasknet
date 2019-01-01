# This code is modified from this source:
# http://adamlamers.com/post/FTPD9KNRA8CT

import sys
import os
import curses
from schclasses import Task, Todo

### TODO: Remove exits
### TODO: Keep command type (it's a generalized way to build menus and is very useful
### TODO: Fast todo traversal (maybe a search completion thing for typing? or vim-like 2w)
### TODO: Format of:
###               title                          expected time               do by
###              [title]                        [exptime]                   [doby]
###                 [title]                     [exptime]                   [doby]
### TODO: Task interaction commands (Add tsk.py functionality)
### TODO: Implement GTD steps: capturing
###                            clarifying (modified for autoscheduling)
###                            ...
###                            task randomization (with the presumption of safety)
### TODO: File separation (good software practice)

class CursesMenu(object): # object here refers to menu_options, which defines how a particular subscreen looks

    ### Todo: Subsetting of tasks

    INIT = {'type' : 'init'}

    def __init__(self, menu_options):
        self.screen = curses.initscr()
        self.menu_options = menu_options
        self.selected_option = 0
        self._previously_selected_option = None
        self.running = True

        #init curses and curses input
        #curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(0) #Hide cursor
        self.screen.keypad(1)

        #set up color pair for highlighted option
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL

    def prompt_selection(self, parent=None):
        if parent is None:
            lastoption = "Exit"
        else:
            # Oh hey, parents are an option!
            lastoption = "Return to previous menu ({})".format(parent['title'])

        option_count = len(self.menu_options['options'])

        input_key = None

        ENTER_KEY = ord('\n')
        while input_key != ENTER_KEY:
            # Not sure why this is here. Maybe a starting condition?
            if self.selected_option != self._previously_selected_option:
                self._previously_selected_option = self.selected_option

            # Highlight relevant option
            self.screen.border(0)
            self._draw_title()
            for option in range(option_count):
                if self.selected_option == option:
                    self._draw_option(option, self.hilite_color)
                else:
                    self._draw_option(option, self.normal_color)


            # Edge condition added so lastoption can be selected.
            if self.selected_option == option_count:
                self.screen.addstr(5 + option_count, 4, "{:2} - {}".format(option_count+1,
                    lastoption), self.hilite_color)
            else:
                self.screen.addstr(5 + option_count, 4, "{:2} - {}".format(option_count+1,
                    lastoption), self.normal_color)

            # Padding.
            max_y, max_x = self.screen.getmaxyx()
            if input_key is not None:
                self.screen.addstr(max_y-3, max_x - 5, "{:3}".format(self.selected_option))
            self.screen.refresh()


            # Move cursor around menu options
            input_key = self.screen.getch()
            down_keys = [curses.KEY_DOWN, ord('j')] # Oh hey, vim!
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]

            if input_key in down_keys:
                if self.selected_option < option_count:
                    self.selected_option += 1
                else:
                    self.selected_option = 0

            if input_key in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count

            # Exit condition
            if input_key in exit_keys:
                self.selected_option = option_count
                break

        return self.selected_option

    def _draw_option(self, option_number, style):
        # Subfunction for drawing "1. Item on menu"
        self.screen.addstr(5 + option_number,
                           4,
                           "{:2} - {}".format(option_number+1, self.menu_options['options'][option_number]['title']),
                           style)

    def _draw_title(self):
        # Subfunction for drawing title
        self.screen.addstr(2, 2, self.menu_options['title'], curses.A_STANDOUT)
        self.screen.addstr(4, 2, self.menu_options['subtitle'], curses.A_BOLD)

    def display(self):
        # Get selected option and send it back out to the output
        selected_option = self.prompt_selection()
        i, _ = self.screen.getmaxyx()
        curses.endwin()
        os.system('clear')
        if selected_option < len(self.menu_options['options']):
            selected_opt = self.menu_options['options'][selected_option]
            return selected_opt
        else:
            self.running = False
            return {'title' : 'Exit', 'type' : 'exitmenu'}

def main():
    todo = Todo()

    menu = {'title' : 'Todo List',
            'type' : 'menu',
            'subtitle' : 'What would you like to edit today?'}

    option_1 = {'title' : 'Hello World',
                'type' : 'command',
                'command' : 'echo Hello World!'}

    option_2 = {'title': 'Does a subtasking thing',
                'type': 'todo'}
                # 'submenu'

    menu['options'] = [option_1,option_2]
    m = CursesMenu(menu)
    selected_action = m.display() # Get an option from the list, and then do something about it

    print(selected_action)

    if selected_action['type'] == 'command':
        os.system(selected_action['command'])

if __name__ == "__main__":
    main()
