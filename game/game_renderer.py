# MAIN RENDERING LOGIC
# Pass in game as dependency
# MountainQuest
# Felix Liu

# Version History
# 5.30.2023 - create file

from utilities.math_utility import *

from game.tilemap import *

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
                match tile:
                    case TileType.FLOOR:
                        char = "."
                    case TileType.WALL:
                        char = "#"
                screen.print_at(char, x, y)
        
        # Render actors
        for a in self.game.actors:
            screen.print_at(a.get_char(), a.get_position().x, a.get_position().y)
