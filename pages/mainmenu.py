import curses

class numberSelectWithTitle:
    """
    Modified from http://adamlamers.com/post/FTPD9KNRA8CT
    Renders something roughly like this:
    Title
        Subtitle
        1. Option 1
        2. Option 2
    """
    def __init__(self, menu_options):
        self.menu_options = menu_options

        # Stuff specific to this page
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0
    
    def _draw_title(self, mainscreen):
        mainscreen.addstr(2, 2, self.menu_options['title'], curses.A_STANDOUT)
        mainscreen.addstr(4, 2, self.menu_options['subtitle'], curses.A_BOLD)
    
    def _draw_option(self, mainscreen, option_number, style):
        mainscreen.addstr(5 + option_number,
                           4,
                           "{:2} - {}".format(option_number + 1, self.menu_options['options'][option_number]['title']),
                           style)

    def show(self, mainscreen):
        self.menu_options['options'].append({'title': 'Exit',
                                             'url': 'exit'})
        
        option_count = len(self.menu_options['options']) # Total options to render
        input_key = None

        ENTER = ord('\n')
        while input_key != ENTER:
            # Draw options
            mainscreen.border(0) # TODO: Is this necessary?
            self._draw_title(mainscreen)
            for option in range(option_count):
                if self.selected_option == option:
                    self._draw_option(mainscreen, option, self.hilite_color)
                else:
                    self._draw_option(mainscreen, option, self.normal_color)

            # Current selection number (bottom right)
            max_y, max_x = mainscreen.getmaxyx()
            if input_key is not None:
                mainscreen.addstr(max_y-3, max_x-5, "{:3}".format(self.selected_option))
            mainscreen.refresh()

            # Wait for key input, then interpret
            input_key = mainscreen.getch()
            down_keys = [curses.KEY_DOWN, ord('j')] # Hi vim users!
            up_keys = [curses.KEY_UP, ord('k')]
            exit_keys = [ord('q')]

            if input_key in down_keys:
                if self.selected_option < option_count - 1:
                    self.selected_option += 1
                else:
                    self.selected_option = 0 # Wraparound
            if input_key in up_keys:
                if self.selected_option > 0:
                    self.selected_option -= 1
                else:
                    self.selected_option = option_count - 1
            
            # Exit condition
            if input_key in exit_keys:
                self.selection_option = option_count - 1 # The exit option
                break
        
        return self.menu_options['options'][self.selected_option]

class mainmenu(numberSelectWithTitle):
    def __init__(self):
        menu = {'title' : 'Todo List',
        'subtitle' : 'What would you like to do?'}
        
        option_1 = {'title' : 'Capturing (task entry)',
                    'url': 'capturing'}
        option_2 = {'title' : 'Clarifying (drill down/add expected time)',
                    'url': 'clarifying'}
        option_3 = {'title' : 'Autoschedule',
                    'url': 'autoschedule'}

        menu['options'] = [option_1, option_2, option_3]

        self.menu_options = menu

        # From the inherited class __init__
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0

    def __call__(self):
        return self