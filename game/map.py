# MAP
# MountainQuest
# Felix Liu

import numpy as np

from utilities.math_utility import *

FLOOR = 0
WALL = 1

VERTICAL = 0
HORIZONTAL = 1
OVERLAP = 2

# Map object, defines the world map, dimensions, and terrain contents
class Map(object):
    # 0 - floor
    # 1 - wall
    # 2 - water

    def __init__(self, dimensions=Vector(32, 32)):
        self.width = dimensions.x
        self.height = dimensions.y
        self.dimensions = dimensions
        self.map = np.zeros(dimensions.get_tuple(), dtype=int)
    def is_in_range(self, position):
        return (position.x >= 0 and position.x < self.width) and (position.y >= 0 and position.y < self.height)
    
    # Getting and setting
    def get_tile(self, position):
        if not self.is_in_range(position):
            raise Exception("Out of map range")
        return self.map[position.x, position.y]
    def set_tile(self, position, tile_id):
        if not self.is_in_range(position):
            raise Exception("Out of map range")
        self.map[position.x, position.y] = tile_id

    # Floor check
    def is_floor(self, position):
        return self.get_tile(position) == FLOOR
    
    # Edit helpers
    def fill(self, tile_id=0):
        self.map.fill(tile_id)