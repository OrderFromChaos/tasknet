# Standard libraries
import os
import json
import curses

# Internal libraries
import pages.pages as pageclasses

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
            'mainmenu' : pageclasses.mainmenu,
            # 'capturing': pageclasses.capturing,
            # 'taskbrowser': pageclasses.taskbrowser,
            # 'contextswitch': pageclasses.contextswitch
        }
        self.meta_urls = {
            'back',
            'exit'
        }
        self.printlog = []
        # Load previous context
        with open('data/meta.json', 'r') as f:
            db = json.load(f)
            self.context = db['logout_context']

        # TODO: Crash handling. Sometimes max UID might be larger than
        #       in meta.json if a TODO was written before the UID update

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
            # Clean up page after exit
            self.screen.clear()
            self.screen.refresh()

    def load(self, url: str):
        if url in self.meta_urls:
            if url == 'exit':
                # TODO: Figure out a proper exit method for curses wrapper
                raise Exception('Exited. Showing print log:\n'
                                '\n'.join(self.printlog))
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
            pageObj = self.page_urls[url](self.context)
            richInfo = pageObj.show(self.screen)

            if 'newcontext' in richInfo: # Pushed by contextswitch
                self.context = richInfo['newcontext']
                with open('data/meta.json', 'r') as f:
                    db = json.load(f)
                db['logout_context'] = self.context
                with open('data/meta.json', 'w') as f:
                    json.dump(db, f, indent=4)

            if 'printlog' in richInfo: # Add log info
                if richInfo['printlog']:
                    self.printlog.append(richInfo['printlog'])

            return richInfo['url']


if __name__ == "__main__":
    # Set up if first run (add 'work' context, add .json files)
    if 'data' not in os.listdir():
        os.mkdir('data')
        with open('data/meta.json', 'w') as f:
            f.write('{\n    "logout_context": "work",\n    "curr_uid": 0\n}')
        os.mkdir('data/work')
        jsonlistfiles = ['finished', 'todo', 'xeffect']
        jsondictfiles = ['settings']
        for jlf in jsonlistfiles:
            with open('data/work/' + jlf + '.json', 'w') as f:
                f.write('[\n\n]')
        for jdf in jsondictfiles:
            with open('data/work/' + jdf + '.json', 'w') as f:
                f.write('{\n\n}')

    # Run main app
    curses.wrapper(PageHandler)
