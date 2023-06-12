# ASCII SCREEN
# Implementations of screen for the ASCIImatics library
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 6.10.2023 - file created

from asciimatics.screen import Screen, ManagedScreen
from utilities.math_utility import *
from enum import IntEnum

import numpy as np

class Color(IntEnum):
    DEFAULT_COLOR = 7
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    TEAL = 6
    BLACK = 0
    WHITE = 7

# Abstract class for input and graphics handling
class ASCIIScreen(object):
    def __init__(self, screen):
        self.graphics = [] # Empty list of ASCII graphics
        self.screen = screen

    def update(self): # Update the current frame
        for graphic in self.graphics:
            graphic.draw(self.screen) # Draw on the current screen
        self.screen.refresh()

    # Add and remove graphics from the screen
    def add_graphic(self, graphic):
        self.graphics.append(graphic)
    def remove_graphic(self, graphic):
        self.graphics.remove(graphic)
    def clear(self):
        self.graphics.clear()

    # SORT GRAPHICS BY SORT ORDER

# GRAPHICS
# Abstract class for a drawable object (can be rendered on screen)
class ASCIIGraphic(object):
    def __init__(self, sort_order=0):
        self.set_sort_order(sort_order)
    def draw(self, screen):
        pass
    def set_sort_order(self, sort_order): # Setting the sort order, with lower numbers drawn below
        self.sort_order = sort_order

# A single ASCII character
class ASCIICharacter(ASCIIGraphic):
    def __init__(self, sort_order=0, char="#", color=Color.DEFAULT_COLOR, point=Vector(0,0)):
        super().__init__(sort_order)
        self.char = char
        self.color = color
        self.point = point
    def draw(self, screen): # Draw the char at its location
        super().draw(screen)
        screen.print_at(self.char, self.point.x, self.point.y, self.color)

# A grid of ASCII graphics
class ASCIIGrid(ASCIIGraphic):
    def __init__(self, sort_order=0, dims=Vector(1,1), pivot=Vector(0,0)): 
        super().__init__(sort_order)
        # Set dims and pivot
        self.dims = dims
        self.pivot = pivot
        # Init grid
        self.grid = np.empty(dims.get_tuple(), dtype=ASCIICharacter)
        for x in range(self.dims.x):
            for y in range(self.dims.y):
                self.grid[x, y] = ASCIICharacter(char=" ", color=Color.DEFAULT_COLOR, point=pivot+Vector(x,y)) # Set each to be an empty ASCII character
    def draw(self, screen): # Draw everything on screen
        for x in range(self.dims.x):
            for y in range(self.dims.y):
                self.grid[x, y].draw(screen) # Draw

# Border around shape
class ASCIIBorder(ASCIIGraphic):
    def __init__(self, sort_order=0, char="#", dims=Vector(0,0), color=Color.DEFAULT_COLOR):
        super().__init__(sort_order)
        self.char = char
        self.dims = dims
        self.color = color
    def draw(self, screen): # Draw the border
        for x in range(self.dims.x + 1):
            screen.print_at(self.char, x, 0, self.color)
            screen.print_at(self.char, x, self.dims.y, self.color)
        for y in range(self.dims.y + 1):
            screen.print_at(self.char, 0, y, self.color)
            screen.print_at(self.char, self.dims.x, y, self.color)

class ASCIIText(ASCIIGraphic):
    def __init__(self, sort_order=0, text="Empty", pivot=Vector(0,0), color=Color.DEFAULT_COLOR):
        super().__init__(sort_order)
        self.text = text
        self.pivot = pivot
        self.color = color
    def draw(self, screen): # Draw the text relative to pivot starting at the top left
        super().draw(screen)
        screen.print_at(self.text, self.pivot.x, self.pivot.y, self.color)
    # Setters/getters
    def set_text(self, text):
        self.text = text
    def get_text(self):
        return self.text