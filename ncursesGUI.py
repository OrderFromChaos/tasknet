# This code is modified from this source:
# https://gist.github.com/claymcleod/b670285f334acd56ad1c

import sys
import os
import curses

class Task:
    def __init__(self, name, expected_length=None, doby=None, duedate=None, children=[]):
        # Everything except name is set to None by default for external imports
        assert type(name) == str
        self.name = name
        self.exptime = expected_length
        self.doby = doby
        self.children = children
    def __repr__(self):
        return str((self.name,self.exptime,self.doby,self.children))
    def __dict__(self):
        # For json serialization
        return {"name":self.name,
                "exptime":str(self.exptime), # Expected to be either None or datetime obj.
                "doby":str(self.doby),
                "children":[x.__dict__() for x in self.children]
                }




def drawMenu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Main loop (k is the last character pressed)
    while (k != ord('q')):

        ### TODO CHANGES:
        # KEY_DOWN, KEY_UP, and the rest need to be doing contextual menu changes, not just [x,y]+-1
        # The relevant context menu choice needs to be highlighted
        # There needs to be key commands per choice (like drill down or like) with the option to cancel

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # TODO This needs to become positional
        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x) # This is a really clean solution that had never occured to me
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        keystr = "Last key pressed: {}".format(k)[:width-1]
        # TODO This needs to become positional or just not display the current thing
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Rendering some text
        

        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(drawMenu)

if __name__ == "__main__":
    main()
