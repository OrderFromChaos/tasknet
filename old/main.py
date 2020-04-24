import os                         # Clearing display at exit
import curses                     # Interface library
# Subpages for CursesWrapper to render
from pages import numberSelectWithTitle, capturingTasks

### TODO: For text input, use curses.textpad
### TODO: Handle exceptions gracefully so as to not break terminal
### TODO: Include subtask lists (eg "main", "beyond2019"), then merge as necessary

class CursesWrapper:
    """
    This class keeps a consistent curses display state, and slots in
    screens to display from other functions.

    Attributes:
        screen:   the screen object from curses.initscr()
        metadata: keeps track of any temp data the subscreens need
    """

    def __init__(self):
        self.screen = curses.initscr()

        # Configure curses
        curses.noecho()          # Curses outputs keys by default, which would be distracting
        curses.cbreak()          # Makes curses react to key presses instantly (no buffer)
        curses.curs_set(False)   # Hide cursor
        curses.start_color()     # Allows for color rendering
        self.screen.keypad(True) # Gracefully handles keys like Page Up
    
    def run(self, startscreen: str):
        # Startscreen is a string URL for the starting page

        # In main, called like this:
        # run('mainmenu')

        # Pseudocode goes something like this:
        # 1. Get mainmenu from a "pagedict" specifying valid pages
        # 2. Render mainmenu using self.render(mainmenuclass)
        #    (By default, pages are given access to the entire screen)
        #    (in other words, curseswrapper trusts the pages to know what they're doing)
        # 3. Asynchronously listen for any page requests
        #    Probably use this:
        #    https://stackoverflow.com/a/14508963/7247528
        #    Shoot, looks like curses is singlethreaded. Fair enough; this was probably a bodge way to do it.
        #    Is there a way to render "atomic" bits of curses code?
        # 4. Load the page request. Some page requests are clearing and so
        #    call self.clear() when that is asked for.
        pass

    def kill(self):
        # TODO: Make sure this gracefully works when subscreens are displayed.
        # curses.nocbreak()
        # self.screen.keypad(False)
        # curses.echo()
        # curses.endwin()
        os.system('clear') # TODO: Is this necessary?

    def render(self,subscreen,page_options):
        """
        Renders an arbitrary subscreen, which represents individual pages of the interface.
        
        Subscreen should be a class that expects a dictionary for
            rendering instructions (hence page_options).
            It should also have a class.show(mainscreen) function.
        
        Returns whatever value class.show(mainscreen) spits out.
        """
        page = subscreen(page_options)
        returnval = page.show(self.screen)
        # self.kill() # TODO: Only here for short-term dev reasons
        return returnval

def main():
    m = CursesWrapper()

    ###################################################
    ###    MAIN PAGE (SELECTING GTDSCH FUNCTION)    ###
    ###################################################
    menu = {'title' : 'Todo List',
            'type' : 'menu',
            'subtitle' : 'What would you like to do?'}
    
    option_1 = {'title' : 'Capturing (task entry)',
                'type': 'screenlink',
                'subscreen': 'capturing'}
    option_2 = {'title' : 'Clarifying (drill down/add expected time)',
                'type': 'screenlink',
                'subscreen': 'clarifying'}
    option_3 = {'title' : 'Autoschedule',
                'type': 'screenlink',
                'subscreen': 'autoschedule'}

    menu['options'] = [option_1, option_2, option_3]

    next_subscreen = m.render(numberSelectWithTitle,menu)

    if next_subscreen['type'] == 'break': # Exit command from main menu
        m.kill()
    elif next_subscreen['title'] == option_1['title']:
        ##################################
        ###    CAPTURING/TASK ENTRY    ###
        ##################################
        screen_options = {'save_each': True, # If true, will write to json for every task input.
                                             #  Else, wll save at end of capturing.
                          'show_old': True,  # If true, will start task scrolldown with tasks
                                             #  most recently added to todo.json.
                          'title':'Capturing',
                          'tip':'Try and write down everything that has an "open loop."'} 
        _ = m.render(capturingTasks, screen_options)
    else:
        m.kill()
        raise NotImplementedError

if __name__ == "__main__": # If this file itself is run
    main()