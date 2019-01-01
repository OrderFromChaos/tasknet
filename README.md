# gtdscheduler

This implements best practices from the book Getting Things Done (capturing, a modified clarifying method) and includes an autoscheduling system for checking if you've overscheduled yourself. The interface is built in ncurses, so it runs in raw Python and should be pretty exportable when finished.

### Current status:
Building the basic system pieces up. 
+ Event objects can be found in schclasses.py. 
+ My first attempt at dialogue can be found in tsk.py.
+ dbaccess.py shows how todo lists get written to a readable/portable json file.
+ Right now, the main file is inside of main.py. The code is a modified boilerplate from online. The landing screen currently works properly.
The end goal is to slot in a bunch of subfeatures into ncursesGUI (like a capturing state) and then implement those nicely. I'm using asciinema for examples of what cool terminal interfaces look like.