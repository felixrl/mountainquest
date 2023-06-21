# MAIN RENDERING LOGIC
# Pass in game as dependency
# MountainQuest
# Felix Liu

# Version History
# 5.30.2023 - create file
# 6.9.2023 - adjusted renderer to not draw walls
# 6.12.2023 - adjusted renderer to draw all non-wall objects as floors
# 6.15.2023 - added UI overlay at the bottom
# 6.20.2023 - added hero stats system for UI overlay

from utilities.math_utility import *
from utilities.color_utility import Color

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
                    case TileType.ENTRANCE:
                        char = "o"
                        color = Color.DEFAULT_COLOR
                    case _:
                        char = "."
                screen.print_at(char, x, y, color)
        
        # Render actors
        for a in self.game.actors:
            screen.print_at(a.get_char(), a.get_position().x, a.get_position().y, a.get_color())

        # UI BOX
        for x in range(self.game.map.width):
            for y in range(10):
                char = " "
                if x == 0 or x == self.game.map.width - 1:
                    char = "|"
                if y == 0 or y == 9:
                    char = "-"
                screen.print_at(char, x, self.game.map.height + y, Color.DEFAULT_COLOR)

        # UI
        # self.render_enemy_list_ui(screen)
        self.render_stats_ui(screen) # RENDER STATS

        # INSTRUCTIONS
        self.print_instructions(screen)
    
    def render_enemy_list_ui(self, screen): # Whose turn? indicator (unused)
        counter = 0
        for a in self.game.actors:
            my_string = "" # Final string
            actor_name = "Enemy" # Most are enemies
            color = Color.DEFAULT_COLOR

            if a == self.game.hero: # Get hero
                actor_name = "Hero"

            if self.game.actors[self.game.current_actor_index] == a: # Current turn
                my_string = "> " + actor_name
                color = Color.YELLOW
            else:
                my_string = actor_name

            # Print at the correct column location, which is map height plus border plus index of this current actor
            screen.print_at(my_string, 2, self.game.map.height + 1 + counter, color)
            counter += 1 # Increment the counter
    
    def render_stats_ui(self, screen): # Hero stats indicator
        color = Color.DEFAULT_COLOR
        screen.print_at("HP | {0}".format(self.game.hero.health), 2, self.game.map.height + 1, color) # HEALTH INDICATOR
        screen.print_at("INVENTORY | {0}".format(self.game.hero.inventory), 2, self.game.map.height + 2, color) # INVENTORY PRINTOUT
    
    # Instructions
    def print_instructions(self, screen):
        screen.print_at("ARROW KEYS: move, Z: drink potion, X: craft potion, S: save map, Q: quit", 2, self.game.map.height + 10 + 1, Color.DEFAULT_COLOR)