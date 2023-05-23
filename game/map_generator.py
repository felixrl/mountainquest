# MAP
# MountainQuest
# Felix Liu

from utilities.math_utility import *
from game.map import *

import random

class Room:
    def __init__(self, pivot=Vector(0,0), dimensions=Vector(15,15)):
        self.pivot = pivot
        self.dimensions = dimensions

# Map object, defines the world map, dimensions, and terrain contents
class MapGenerator(object):
    def __init__(self, dimensions=Vector(32, 32)):
        self.create_new_map(dimensions)
    
    def get_map(self):
        return self.new_map
    
    # Creates a new empty map (all 0)
    def create_new_map(self, dimensions=Vector(32, 32)):
        self.new_map = Map(dimensions)
    def fill_with_wall(self):
        self.new_map.fill(WALL)

    # ROGUE GENERATION
    def generate_rogue(self, dimensions, cols=3, rows=3):
        self.create_new_map(dimensions)
        self.fill_with_wall()
        self.grid_cell_dimensions = Vector(int(dimensions.x/cols), int(dimensions.y/rows))
        self.room_grid = np.zeros((cols, rows), dtype=Room)

        for x in range(cols):
            for y in range(rows):
                point = Vector(x, y)
                pivot = self.get_rogue_room_pivot(point)
                dims = self.get_rogue_room_dim()
                new_room = Room(pivot, self.get_rogue_room_dim())
                self.room_grid[x, y] = new_room

        for x in range(cols):
            for y in range(rows):
                continue
                self.apply_room(self.room_grid[x, y])

        points = self.determine_prime_path(Vector(0, 0))

    def get_rogue_room_pivot(self, point=Vector()):
        x = point.x * self.grid_cell_dimensions.x + 1
        y = point.y * self.grid_cell_dimensions.y
        return Vector(int(x), int(y))
    def get_rogue_room_dim(self):
        x = random.randint(4, self.grid_cell_dimensions.x - 1)
        y = random.randint(4, self.grid_cell_dimensions.y - 1)
        return Vector(x, y)
    
    def determine_prime_path(self, point=Vector(), points=[]):
        points.append(point)

        option = random.randint(0,2)
        match option:
            case 0: # RIGHT
                return self.determine_prime_path(point + Vector(1, 0), points)
            case 1: # UP
                return self.determine_prime_path(point - Vector(0, 1), points)
            case 2: # DOWN
                return self.determine_prime_path(point + Vector(0, 1), points)
        return points

    # GENERATE ROGUE-STYLE ROOMS CONNECTED BY CORRIDORS
    def generate_dungeon_rooms(self, dimensions, num_of_rooms=10):
        self.create_new_map(dimensions)
        self.fill_with_wall()

        rooms = []
        room_counter = 0
        while room_counter < num_of_rooms:
            new_room = self.attempt_generate_room()
            if new_room == -1:
                continue
            rooms.append(new_room)
            room_counter += 1
            self.apply_room(new_room)
        
        # for r in rooms:
            # self.apply_room(r)
    
    def attempt_generate_room(self):
        # generate random coords
        pivot = Vector(random.randint(0, self.new_map.width), random.randint(0, self.new_map.height))
        dims = Vector(random.randint(10, 20), random.randint(5, 10))
        
        if not self.new_map.is_in_range(pivot) or not self.new_map.is_in_range(pivot + dims):
            return -1
        for x in range(dims.x):
            for y in range(dims.y):
                offset = Vector(x, y)
                if self.new_map.get_tile(pivot + offset) == FLOOR:
                    return -1
        
        # Check padding
        for x in range(dims.x + 2):
            for y in range(dims.y + 2):
                offset = Vector(x, y)
                new_pivot = pivot - Vector(1, 1)
                if not self.new_map.is_in_range(new_pivot + offset):
                    return -1
                if self.new_map.get_tile(new_pivot + offset) == FLOOR:
                    return -1

        return Room(pivot, dims)
    
    def apply_room(self, room):
        # actually generate it
        for x in range(room.dimensions.x):
            for y in range(room.dimensions.y):
                offset = Vector(x, y)
                self.new_map.set_tile(room.pivot + offset, FLOOR)

    # GENERATE A MAP CONTAINING DISTANCES FROM A CHOSEN "SPAWN POINT"
    def generate_distance_map(self, start=Vector(0,0)):
        # FILL CODE IN
        pass