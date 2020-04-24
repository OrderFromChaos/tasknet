import os
import curses
import pages.pages as pageclass

class PageHandler:
    """
    Loads new pages when sent a "URL" as part of the return 
    from the last loaded page.
    """
    def __init__(self, screen):
        # Class variables
        self.screen = screen
        self.currenturl = ''
        self.urlhistory = []  # Allows for commands like "back"
        self.page_urls = { # Don't forget to index your pages here!
            'mainmenu' : pageclass.mainmenu,
            'capturing': pageclass.capturing
        }
        self.meta_urls = {
            'back',
            'exit'
        }
        self.context = 'work'

        # Set up global curses settings
        curses.noecho()          # Curses outputs keys by default, 
                                 #     which would be distracting
        curses.cbreak()          # Makes curses react to keypresses 
                                 #     instantly (no buffer)
        curses.curs_set(False)   # Hide cursor
        curses.start_color()     # Allows for color rendering
        curses.use_default_colors() # Fixes some errors
        for i in range(0, curses.COLORS): # Initialize colors to 1, 2, ...
            curses.init_pair(i + 1, i, -1)
        self.screen.keypad(True) # Gracefully handles keys like "Page Up"

        # Start main loop
        self.run()

    
    def run(self):
        nexturl = self.load('mainmenu')
        self.screen.clear()
        self.screen.refresh()
        while True: # self.load() already does validity checks, no need to here
            nexturl = self.load(nexturl)
            # Clean up page
            self.screen.clear()
            self.screen.refresh()

    def load(self, url: str):
        if url in self.meta_urls:
            if url == 'exit':
                exit(0)
            elif url == 'back':
                if not self.urlhistory:
                    raise Exception('Back called on an empty history stack')
                else:
                    url = self.urlhistory[-1]
        
        if url not in self.page_urls:
            raise Exception(f'Invalid URL requested: "{url}"\n'
                            '(DEV HINT: Did you forget to add your page'
                            'to self.page_urls?)')
        else:
            pageObj = self.page_urls[url]()
            richInfo = pageObj.show(self.screen, self.context)
            # TODO: Figure out a use for the rest of this richInfo.
            # Perhaps subpages could set global curses display settings?
            return richInfo['url']

if __name__ == "__main__":
    curses.wrapper(PageHandler)
