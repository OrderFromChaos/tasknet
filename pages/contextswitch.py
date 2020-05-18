import os
import bisect
import curses
import curses.textpad as textpad

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
        self.currcontext = context
        self.allcontexts = [f.path for f in os.scandir('data') if f.is_dir()]
        self.allcontexts = [x.split('/')[-1] for x in self.allcontexts]
        self.allcontexts.sort()
        self.contextindex = bisect.bisect_left(self.allcontexts, self.currcontext)
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
            add_keys = [ord('a')]

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
            elif userinput in add_keys:
                # Make a text box underneath everything
                max_y, max_x = mainscreen.getmaxyx()
                textwindow = curses.newwin(1, max_x//2, 2+len(neighborhood)+1, 2)
                box = textpad.Textbox(textwindow, insert_mode=True)
                contents = box.edit()
                del textwindow

                contents = contents.strip()

                newdir = 'data/' + contents + '/'
                os.mkdir(newdir)
                jsonlistfiles = ['finished', 'todo', 'xeffect']
                jsondictfiles = ['settings']
                for jlf in jsonlistfiles:
                    with open(newdir + jlf + '.json', 'w') as f:
                        f.write('[\n\n]')
                for jdf in jsondictfiles:
                    with open(newdir + jdf + '.json', 'w') as f:
                        f.write('{\n\n}')

                bisect.insort_left(self.allcontexts, contents)
                self.currcontext = contents
                self.contextindex = bisect.bisect_left(self.allcontexts, self.currcontext)
                # TODO: Need to filter out bad characters like " "
            elif userinput == ord('\n'):
                self.currcontext = self.allcontexts[self.contextindex]
                break

            mainscreen.clear()
            mainscreen.refresh()

        returndict = {
            'url': 'mainmenu',
            'newcontext': self.currcontext
        }

        return returndict