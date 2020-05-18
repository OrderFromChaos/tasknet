import os
from bisect import bisect_left
import curses

class contextswitch:
    # Want contexts to be searchable easily
    # "a" for adding context
    # "d" for context deletion UI (are you sure? currently has X tasks; show a few of them)
    #     no by default (of course)
    # "e" to rename (input box needs option to prefill)
    # "s" -> alpha input with bisect_left on each step
    #     shift-enter to immediately switch to said context
    # scrolling ui, a la old school rotary phones
    # TODO: add context indicator on other pages
    def __init__(self, context):
        self.startcontext = context
        self.allcontexts = [f.path for f in os.scandir('data') if f.is_dir()]
        self.allcontexts = [x.split('/')[-1] for x in self.allcontexts]
        self.allcontexts.sort()
        self.contextindex = bisect_left(self.allcontexts, self.startcontext)
    def show(self, mainscreen):
        # Grab the nearby 2 adjacent contexts and
        #   shove it into a list [c-2, c-1, c, c+1, c+2]
        while True:
            neighborhood = []
            for i in range(self.contextindex-2, self.contextindex+3):
                if i < 0 or i > len(self.allcontexts)-1:
                    neighborhood.append("")
                else:
                    neighborhood.append(self.allcontexts[i])
            
            # Display as rotary menu
            spacing = 2
            midpoint = len(neighborhood)//2
            for i in range(len(neighborhood)):
                if i == midpoint:
                    mainscreen.addstr(2+i, 
                                      2, 
                                      neighborhood[i])
                else:
                    mainscreen.addstr(2+i, 
                                      2+spacing*abs(midpoint-i), 
                                      neighborhood[i])
            
            # Capture keys
            down_keys = [curses.KEY_DOWN, ord('j')] # Hi vim users!
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]

            userinput = mainscreen.getch()

            if userinput in down_keys:
                if self.contextindex < len(self.allcontexts) - 1:
                    self.contextindex += 1
                else:
                    pass # Do nothing
            elif userinput in up_keys:
                if self.contextindex > 0:
                    self.contextindex -= 1
                else:
                    pass # Do nothing
            elif userinput in exit_keys:
                break
            # elif userinput == ord('\n'):

            mainscreen.clear()
            mainscreen.refresh()


        return {'url': 'mainmenu'}