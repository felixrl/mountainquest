# MAP
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.26.2023 - File created

from utilities.math_utility import *

from enum import IntEnum
import numpy as np

class TileType(IntEnum):
    FLOOR = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3

# A map of tiles
class Tilemap:
    def __init__(self, dimensions=Vector(32, 32)):
        self.map = np.zeros(dimensions.get_tuple(), dtype=TileType)

    # Getter/setter
    def get_tile(self, position=Vector()):
        return self.map[position.x, position.y]
    def set_tile(self, position=Vector(), tile_type=TileType.FLOOR):
        self.map[position.x, position.y] = tile_type