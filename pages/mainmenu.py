import pages.common as common
import curses

class mainmenu(common.numberSelectWithTitle):
    def __init__(self, context):
        self.context = context
        
        menu = {'title' : 'Main menu',
        'subtitle' : 'What would you like to do?'}
        
        options = [
            {
                'title': 'Capturing (task entry)',
                'url': 'capturing'
            },
            {
                'title': 'Clarifying (drill down/add expected time)',
                'url': 'clarifying'
            },
            {
                'title': 'Browse tasks',
                'url': 'taskbrowser'
            },
            {
                'title': 'Autoschedule',
                'url': 'autoschedule'
            },
            {
                'title': 'Switch contexts',
                'url': 'contextswitch' 
            }
        ]

        menu['options'] = options

        self.menu_options = menu

        # From the inherited class __init__
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.hilite_color = curses.color_pair(1)
        self.normal_color = curses.A_NORMAL
        self.selected_option = 0
