# TILEMAP
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.26.2023 - File created
# 6.16.2023 - Updated for better implementation, moved is_contiguous check and other helper functions

from utilities.math_utility import *

from enum import IntEnum
import numpy as np

# Enum for distinguishing between various tile types (https://docs.python.org/3/library/enum.html)
class TileType(IntEnum):
    FLOOR = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3
    ENEMY_SPAWNER = 4

# A map of tiles
class TileMap:
    def __init__(self, dimensions=Vector(32, 32)):
        self.width = dimensions.x
        self.height = dimensions.y
        self.map = np.zeros(dimensions.get_tuple(), dtype=TileType) # Create a 2D map with the TileType datatype

    # Getter/setter
    def get_tile(self, position=Vector()):
        if self.is_in_range(position): # Only get if in map range
            return self.map[position.x, position.y]
        else:
            print("Attempted get tile ({0}) out of map range!".format(position))
            return TileType.WALL # Return a wall outside map range to prevent escaping
    def set_tile(self, position=Vector(), tile_type=TileType.FLOOR):
        if self.is_in_range(position): # Only set if in map range
            self.map[position.x, position.y] = tile_type
        else:
            print("Attempted set tile ({0}) out of map range!".format(position))

    # Helper functions
    def is_in_range(self, position): # Check if the position is in range
        return (position.x >= 0 and position.x < self.width) and (position.y >= 0 and position.y < self.height)
    def is_contiguous(self, position=Vector(0,0)): # Check if the tile is bounded by similar tiles in all 8 directions
        contiguous = True
        directions = [Vector(1,0), Vector(0,1), Vector(-1,0), Vector(0,-1), Vector(1,1), Vector(-1,-1), Vector(1,-1), Vector(-1,1)]
        for d in directions: # For each direction
            new_position = position + d
            if self.is_in_range(new_position): # Is it in range? (Out of range is considered contiguous)
                if self.get_tile(new_position) != self.get_tile(position): # Not contiguous, different tile
                    contiguous = False
        return contiguous
    def is_tile_type(self, position=Vector(0,0), tile_type=TileType.FLOOR): # Check if tile is of type
        return self.get_tile(position) == tile_type
    def fill(self, tile_type=TileType.FLOOR): # Fill entire map with a type of tile
        self.map.fill(tile_type)