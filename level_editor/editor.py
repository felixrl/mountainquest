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

# Mapping TileType to names
TileNames = {
    TileType.FLOOR: "Floor",
    TileType.WALL: "Wall",
    TileType.ENTRANCE: "Entrance (Only one allowed)",
    TileType.EXIT: "Exit (Only one allowed)",
    TileType.ENEMY_SPAWNER: "Enemy"
}

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
        if self.get_tile(position) == TileType.ENTRANCE or self.get_tile(position) == TileType.EXIT: # DON'T ALLOW REPLACING OF ENTRANCE OR EXIT
            return
        if self.selected_tile_type == TileType.ENTRANCE or self.selected_tile_type == TileType.EXIT: # MOVING ENTRANCE OR EXIT, ONLY ONE
            for x in range(self.map.width): # Loop through
                for y in range(self.map.height):
                    # Logic conditions, only remove when moving the same type
                    entrance_found = (self.selected_tile_type == TileType.ENTRANCE and self.get_tile(Vector(x,y)) == TileType.ENTRANCE)
                    exit_found = (self.selected_tile_type == TileType.EXIT and self.get_tile(Vector(x,y)) == TileType.EXIT)
                    if entrance_found or exit_found:
                        self.map.set_tile(Vector(x,y), TileType.FLOOR) # Replace the existing entrance with floor

        self.map.set_tile(position, self.selected_tile_type) # Set the tile
    
    # GET TILE
    def get_tile(self, position=Vector(0,0)):
        return self.map.get_tile(position)