# needs to accept recursive todos
# display todo information on the side
# needs to be scrollable (todo list might be long)
# needs to cut todo names down if they're too long

class taskbrowser:
    def __init__(self, context):
        self.context = context

    def show(self, mainscreen):
        info = self.getContent()

        while True:
            # make two windows;
            # left for name info,
            # right for metadata
            
            # left window
            indent = '  '
            row = 2
            stack = [(x, 0) for x in info]
            while len(stack):
                entry, depth = stack.pop()
                name, metadata, children = entry

                mainscreen.addstr(row, 2+depth, name)
                row += 1

                if children:
                    stack += [(x, depth+1) for x in children]

            userinput = mainscreen.getch()
            if userinput == ord('q'):
                break
        
        return {'url': 'mainmenu'}

    def getContent(self):
        # Needs to return list of 3-length tuples
        # (display on line, metadata, children)
        # metadata is a dict
        example1 = (
            'Content example 1',
            {
                'due date': 'Thursday 5pm'
            },
            [
                (
                    'Content example 2',
                    {
                        'due date': 'Friday 10am'
                    },
                    []
                )
            ]
        )
        example2 = (
            'Content example 3',
            {
                'due date': '3 weeks'
            },
            []
        )
        return [example1, example2]

    