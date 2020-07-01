# Normal textpad doesn't allow for normal backspace
# Normal textpad doesn't allow char filtering
# Normal textpad doesn't allow for repositioning (afaik),
    # meaning window borders get overwritten
# Normal textpad doesn't let you do ctrl+q to exit 
# Normal textpad doesn't let you initialize with contents
# Normal textpad doesn't remove the tailing space by default
# (The custom version does let you do these things!)
    # (TODO: Except for ctrl+q to exit)

# Old textpad interface:
    # textwindow = curses.newwin(nrows, ncols, startx, starty)
    # box = textpad.Textbox(textwindow, insert_mode=True)
    # contents = box.edit()
    # del textwindow
    # contents = contents.strip()
    # self.tasks[self.addtask.uid].name = contents

import curses
from string import ascii_lowercase, ascii_uppercase

class CustomTextbox:
    def __init__(self,
                 window, # Window to draw textbox in
                 contents=[], # Pre-initializing textbox
                 charfilter=set(), # If non-empty, only these chars are accepted
                 border=False # If True, textbox is verti-centered and shifted right 1
                 ):
        self.window = window
        self.contents = contents
        if isinstance(self.contents, str):
            self.contents = list(contents)
        if charfilter:
            if isinstance(charfilter, list):
                charfilter = set(charfilter)
            self.filter = charfilter
        else:
            self.filter = (ascii_lowercase 
                           + r"""`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}\|;:'",<.>/? """
                           + ascii_uppercase)
            self.filter = set(self.filter)
        self.border = border
    def edit(self):
        last = None # TODO: Use this for catching control sequences (eg CTRL)

        while True:
            # 1. Draw window
            self.window.clear()
            self.window.refresh()

            if not self.border:
                self.window.addstr(0, 0, ''.join(self.contents))
            else:
                self.window.border()
                max_y, max_x = self.window.getmaxyx()
                self.window.addstr(max_y//2, 1, ''.join(self.contents))

            # 2. Key processing
            c = self.window.getch()
            if c == ord('\n'):
                break
            elif c == 127:
                if self.contents:
                    self.contents.pop()
            # TODO: catch ctrl/alt patterns
            
            if chr(c) not in self.filter:
                continue
            
            self.contents.append(chr(c))
        
        return ''.join(self.contents)


        
