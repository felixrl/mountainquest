# MAIN RENDERING LOGIC
# Pass in game as dependency
# MountainQuest
# Felix Liu

# Version History
# 5.30.2023 - create file
# 6.9.2023 - adjusted renderer to not draw walls
# 6.12.2023 - adjusted renderer to draw all non-wall objects as floors
# 6.15.2023 - added UI overlay at the bottom

from utilities.math_utility import *

from game.tilemap import *

from enum import IntEnum

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

class GameRenderer(object):
    def __init__(self, game=None):
        self.game = game

    def render(self, screen):
        if self.game == None:
            raise Exception("No game to render!")

        # Render map
        for x in range(self.game.map.width):
            for y in range(self.game.map.height):
                tile = self.game.map.get_tile(Vector(x, y))
                char = " "
                color = Color.DEFAULT_COLOR
                match tile:
                    case TileType.FLOOR:
                        char = "."
                    case TileType.WALL:
                        char = "#"
                        if self.game.map.is_contiguous(Vector(x,y)):
                            char = " "
                        char=" "
                    case TileType.EXIT:
                        char = "L"
                        color = Color.YELLOW
                    case _:
                        char = "."
                screen.print_at(char, x, y, color)
        
        # Render actors
        for a in self.game.actors:
            screen.print_at(a.get_char(), a.get_position().x, a.get_position().y, a.get_color())

        # UI TEST
        for x in range(self.game.map.width):
            for y in range(10):
                char = " "
                if x == 0 or x == self.game.map.width - 1:
                    char = "|"
                if y == 0 or y == 9:
                    char = "-"
                screen.print_at(char, x, self.game.map.height + y, Color.DEFAULT_COLOR)

        counter = 0
        for a in self.game.actors:
            my_string = ""
            actor_name = "Actor"
            color = Color.DEFAULT_COLOR

            if a == self.game.hero:
                actor_name = "Hero"

            if self.game.actors[self.game.current_actor_index] == a:
                my_string = "> " + actor_name
                color = Color.YELLOW
            else:
                my_string = actor_name

            screen.print_at(my_string, 2, self.game.map.height + 1 + counter, color)
            counter += 1