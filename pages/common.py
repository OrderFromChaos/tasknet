import curses
from core.customtextbox import CustomTextbox

class numberSelectWithTitle:
    """
    Modified from http://adamlamers.com/post/FTPD9KNRA8CT
    Renders something roughly like this:
    Title
        Subtitle
        1. Option 1
        2. Option 2
    """
    def __init__(self, context):
        self.context = context
        self.menu_options = []

        # Stuff specific to this page
        curses.init_pair(500, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(500)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0
    
    def _draw_title(self, mainscreen):
        # mainscreen.addstr(2, 2, self.menu_options['title'], curses.A_STANDOUT)
        mainscreen.addstr(2, 2, self.menu_options['subtitle'], curses.A_BOLD)
    
    def _draw_option(self, mainscreen, option_number, style):
        mainscreen.addstr(3 + option_number,
                           4,
                           "{:2} - {}".format(option_number + 1, 
                           self.menu_options['options'][option_number]['title']),
                           style)

    def show(self, mainscreen):
        self.menu_options['options'].append({'title': 'Exit',
                                             'url': 'exit'})
        
        option_count = len(self.menu_options['options']) # Total options to render
        input_key = None

        # Define key types
        down_keys = [curses.KEY_DOWN, ord('j')] # Hi vim users!
        up_keys = [curses.KEY_UP, ord('k')]
        exit_keys = [ord('q')]
        numbers = {ord(str(x)) for x in range(1, 10)}
        ENTER = ord('\n')

        
        while input_key != ENTER:
            # Draw options
            # mainscreen.border(0)
            self._draw_title(mainscreen)
            for option in range(option_count):
                if self.selected_option == option:
                    self._draw_option(mainscreen, option, self.hilite_color)
                else:
                    self._draw_option(mainscreen, option, self.normal_color)

            # Current selection number (bottom right)
            max_y, max_x = mainscreen.getmaxyx()
            mainscreen.addstr(1, 2, f"[{self.context}]", curses.A_BOLD)
            # mainscreen.refresh()

            # Wait for key input, then interpret
            input_key = mainscreen.getch()

            if input_key in down_keys:
                if self.selected_option < option_count - 1:
                    self.selected_option += 1
                else:
                    self.selected_option = 0 # Wraparound
            elif input_key in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count - 1
            elif input_key in numbers:
                expected = int(chr(input_key)) - 1
                # negatives are multiple chars; ignored for now
                # numbers includes 1-9

                if expected < option_count:
                    self.selected_option = expected
                else:
                    self.selected_option = option_count - 1
                
                return self.menu_options['options'][self.selected_option]
            
            # Exit condition
            if input_key in exit_keys:
                self.selected_option = option_count - 1 # The exit option
                break
        
        return self.menu_options['options'][self.selected_option]

class inputWithScrollBack:
    def __init__(self, context):
        self.context = context
        self.history = []
        self.prompt = ''
    def show(self, mainscreen):
        # lines 2-3 are reserved for the current prompt and the text input box
        # lines 4-> are history (progresively greyed out)
        self.start()

        contents = ''
        while contents not in {'exit', 'q'}:
            prompt = self.generateprompt()
            
            mainscreen.clear()

            mainscreen.addstr(2, 2, prompt, curses.A_BOLD)
            # Render history
            for i, x in enumerate(self.history[-10:][::-1]):
                mainscreen.addstr(5+i, 4, x, curses.color_pair(247-i))

            mainscreen.refresh()
            textwindow = curses.newwin(1, mainscreen.getmaxyx()[1], 3, 4)
            box = CustomTextbox(textwindow, contents='')
            contents = box.edit()
            del textwindow

            if contents not in {'exit', 'q', ''}:
                self.history.append(contents)
                self.dostuff(contents)
        
        self.cleanup()
        
        return {'url': self.exiturl()}
    
    def generateprompt(self) -> str:
        return self.prompt

    def dostuff(self):
        pass

    def exiturl(self):
        return 'mainmenu'
    
    def start(self):
        pass
    
    def cleanup(self):
        pass

def validate_input(userinput, method) -> str:
    # Accepts either a regex string or a function that returns a bool
    # Returns the validated string
    assert (isinstance(method, str) or callable(method))
    while True:
        if isinstance(method, str):
            regex = re.compile(method)
            if regex.findall(userinput)[0] == userinput:
                return userinput
            else:
                print('Looks like you made a typo. Try again!')
        else:
            if method(userinput):
                return userinput
            else:
                print('Looks like you made a typo. Try again!')

class spreadSheetWithSidebar: # May be useful, currently mothballed due to infinite recursive depth allowance
    def __init__(self, data):
        self.data = []
        self.displaykeys = []
        self.sidebarsize = 20
    def show(self, mainscreen):
        pass

    