# EDITOR RENDERING LOGIC
# Pass in game as dependency
# MountainQuest
# Felix Liu

# Version History
# 6.20.2023 - file created for level editor rendering

from utilities.math_utility import *
from utilities.color_utility import Color

from game.tilemap import *

class EditorRenderer(object):
    def __init__(self, editor=None):
        self.editor = editor

    def render(self, screen):
        if self.editor == None:
            raise Exception("No editor to render!")

        # Render map
        for x in range(self.editor.map.width):
            for y in range(self.editor.map.height):
                tile = self.editor.map.get_tile(Vector(x, y))
                char = " "
                color = Color.DEFAULT_COLOR
                match tile:
                    case TileType.FLOOR:
                        char = "."
                    case TileType.WALL:
                        char = "#"
                        if self.editor.map.is_contiguous(Vector(x,y)):
                            char = " "
                        char=" "
                    case TileType.EXIT:
                        char = "L"
                        color = Color.YELLOW
                    case TileType.ENTRANCE:
                        char = "@"
                        color = Color.DEFAULT_COLOR
                    case TileType.ENEMY_SPAWNER: # Enemy spawner
                        char = "e"
                        color = Color.RED
                    case _:
                        char = "."
                screen.print_at(char, x, y, color)

        # UI BOX
        for x in range(self.editor.map.width):
           for y in range(10):
               char = " "
               if x == 0 or x == self.editor.map.width - 1:
                   char = "|"
               if y == 0 or y == 9:
                   char = "-"
               screen.print_at(char, x, self.editor.map.height + y, Color.DEFAULT_COLOR)

        self.render_stats_ui(screen)

        # INSTRUCTIONS
        self.print_instructions(screen)
    
    def render_stats_ui(self, screen): # Selection indicator
        color = Color.DEFAULT_COLOR
        screen.print_at("SELECTED TILE | {0}".format(self.editor.selected_tile_type), 2, self.editor.map.height + 1, color)

    # Instruction printing, keys avaliable
    def print_instructions(self, screen):
        screen.print_at("Q: quit, G: generate a random rogue map, 1-5: select tile type", 2, self.editor.map.height + 10 + 1, Color.DEFAULT_COLOR)