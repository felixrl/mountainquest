# CURSES SCREEN
# MountainQuest
# Felix Liu

from utilities.math_utility import *
from enum import IntEnum

import numpy as np
import curses

class Color(IntEnum):
    DEFAULT_COLOR = curses.COLOR_WHITE
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE
    PURPLE = curses.COLOR_MAGENTA
    TEAL = curses.COLOR_CYAN
    BLACK = curses.COLOR_BLACK
    WHITE = curses.COLOR_WHITE



# ------
# SCREEN
# ------

# A display GUI powered by Curses
class CursesScreen(object):
    def __init__(self, input_handler=None, graphics=[]):
        self.screen = curses.initscr()
        # Curses configuration
        curses.noecho() # Disable key echoing
        curses.cbreak() # Disable input buffering
        curses.start_color() # Setup color support

        self.screen.keypad(True) # Enable keypad mode for keys like arrows, specials, etc

        # GRAPHICS
        self.graphics = graphics

        # INPUT
        self.input_handler = input_handler

        self.active = True

    def add_graphic(self, graphic):
        self.graphics.append(graphic)
    def remove_graphic(self, graphic):
        self.graphics.remove(graphic)

    def update(self):
        try:
            self.screen.clear()
            for graphic in self.graphics: # Loop through all graphics and
                graphic.draw(self.screen) # call draw
            self.screen.refresh()
        except: # An error occurred.
            self.end()
            raise Exception("An error occured in updating Curses.")
    def update_input(self):
        input_code = self.screen.getch()
        self.input_handler.handle_input(input_code)
        if input_code == ord("q"): # QUIT CODE
            self.end()

    def end(self):
        # Closing curses
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        self.active = False



# -----
# INPUT
# -----

class CursesInputHandler(object):
    def __init__(self, handle):
        self.handle = handle
    def handle_input(self, e):
        self.handle(e) # Delegate response to an external function



# --------
# GRAPHICS
# --------

# Extensible graphics objects 
# Abstract graphic (drawable)
class Graphic(object):
    id_counter = 1

    def __init__(self):
        pass
    def draw(self, screen):
        pass

# Graphic for a text object (character, string, title, etc)
class TextGraphic(Graphic):    
    def __init__(self, text="Undefined", pivot=Vector(0,0), text_color=Color.DEFAULT_COLOR, background_color=Color.BLACK): # The text pivot is located on the top-left
        self.text = text
        self.pivot = pivot
        self.text_color = text_color
        self.background_color = background_color
        # Track graphics with a constantly incrementing ID value
        self.id = Graphic.id_counter
        Graphic.id_counter += 1

    def draw(self, screen):
        # https://docs.python.org/3/howto/curses.html#:~:text=They%20are%3A%200%3Ablack%2C,each%20of%20these%20colors%3A%20curses.
        curses.init_pair(self.id, self.text_color, self.background_color) # Create the color pair
        # First argument defines character, second argument defines line
        screen.addstr(self.pivot.y, self.pivot.x, self.text, curses.color_pair(self.id)) # Add the string to the screen
# Graphic for a grid of graphics
class GridGraphic(Graphic):
    def __init__(self, dims=Vector(1,1)):
        self.grid = np.empty(dims.get_tuple(), dtype=Graphic)
        self.dims = dims
    def draw(self, screen):
        for x in range(self.dims.x):
            for y in range(self.dims.y):
                self.grid[x, y].pivot = Vector(x, y)
                self.grid[x, y].draw(screen)
    
    def set_graphic(self, graphic=None, point=Vector(0,0)):
        self.grid[point.x, point.y] = graphic
