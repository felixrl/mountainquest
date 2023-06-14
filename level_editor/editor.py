# Level Editor
# MountainQuest
# Felix Liu

# Version History
# 6.12.2023 - File created. Prototyping editor.

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.event import MouseEvent

# from utilities.math_utility import *

with ManagedScreen() as screen: # Create screen with screen context
    # screen.print_at("hi", 0, 0)
    start_point = None
    while True:
        e = screen.get_event()
        if type(e) == type(MouseEvent(0,0, None)): # If it is a mouse event
            print(e)
            screen.clear()
            screen.print_at("({0}, {1})".format(e.x, e.y), 0, 0)
            screen.print_at("+", e.x, e.y) # Cursor
            if e.buttons == MouseEvent.LEFT_CLICK:
                screen.print_at("hi", 20, 20)
        screen.refresh()