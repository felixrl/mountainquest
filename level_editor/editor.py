# Level Editor
# MountainQuest
# Felix Liu

# Version History
# 6.12.2023 - File created. Prototyping editor.
# 6.21.2023 - Added implementation for LevelEditor

from utilities.math_utility import Vector

from asciimatics.screen import Screen, ManagedScreen
from asciimatics.event import MouseEvent

from game.tilemap import TileType

# LEVEL EDITOR OBJECT, keeps reference to a TileMap to edit
class LevelEditor(object):
    def __init__(self, map):
        self.map = map
        self.selected_tile_type = TileType.FLOOR

    # Set the selected tile to set
    def set_selected_tile(self, tile_type=TileType.FLOOR):
        self.selected_tile_type = tile_type

    # Set to selected tile
    def set_tile(self, position=Vector(0,0)):
        self.map.set_tile(position, self.selected_tile_type)
    
    # GET TILE
    def get_tile(self, position=Vector(0,0)):
        return self.map.get_tile(position)