import os
import curses
import pages.pages

class PageHandler:
    """
    Loads new pages when sent a "URL" as part of the return 
    from the last loaded page.
    """
    def __init__(self, screen):
        self.screen = screen
        self.urlhistory = []  # Allows for commands like "back"
        self.page_urls = { # Don't forget to index your pages here!
            'mainmenu'
        }
        self.meta_urls = {
            'back',
            'exit'
        }
    def load(self, url: str):
        if url in meta_urls:
            pass # TODO
        if url in allowed_urls:
            pass

if __name__ == "__main__":
    curses.wrapper(PageHandler)
