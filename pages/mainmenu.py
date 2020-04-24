import pages.common as common
import curses

class mainmenu(common.numberSelectWithTitle):
    def __init__(self):
        menu = {'title' : 'Main menu',
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