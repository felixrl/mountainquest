# MAP
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.23.2023 - Began work on room connection system, prime path finder
# 5.25.2023 - Added demo map generator for full room, recursive function for generating a distance map with flood fill
# 6.1.2023 - Added function for creating a wall block

from utilities.math_utility import *
from game.map import *

import random
import sys

# A room class defining pivot, dimensions, and connections
class Room:
    def __init__(self, pivot=Vector(0,0), dimensions=Vector(15,15)):
        self.pivot = pivot
        self.dimensions = dimensions
        self.connected_rooms = []

    # Functions for manipulating room connections
    def connect(self, room):
        self.connected_rooms.append(room)
    def disconnect(self, room):
        self.connected_rooms.remove(room)

# A class defining a grid of rooms
class RoomGrid:
    def __init__(self, dimensions=Vector(3,3)):
        self.room_grid = np.zeros(dimensions.get_tuple(), dtype=Room)
    
    def set_room(self, point, room):
        self.room_grid[point.x, point.y] = room
    def get_room(self, point):
        return self.room_grid[point.x, point.y]

    def scalar_index_to_2d(self, i):
        x = i % self.room_cols
        y = i // self.room_rows
        return Vector(x, y)
    def get_at_scalar_index(self, i):
        point = self.scalar_index_to_2d(i)
        return self.room_grid[point.x, point.y]


# Map object, defines the world map, dimensions, and terrain contents
class MapGenerator(object):
    def __init__(self, dimensions=Vector(32, 32)):
        self.create_new_map(dimensions)
    
    # GET ACCESS TO THE FINISHED MAP
    def get_map(self):
        return self.new_map
    
    # MAP CREATION FUNCTIONS
    # Creates a new empty map (all 0s)
    def create_new_map(self, dimensions=Vector(32, 32)):
        self.new_map = Map(dimensions)
    def fill_with_wall(self):
        self.new_map.fill(WALL)

    # Add a block of wall
    def add_wall_block(self, pivot=Vector(0,0), size=Vector(10,10)):
        for x in range(size.x):
            for y in range(size.y):
                new_pos = pivot + Vector(x, y)
                if self.new_map.is_in_range(new_pos):
                    self.new_map.set_tile(new_pos, WALL)

    def create_dumb_map(self, dimensions=Vector(32, 32)):
        # Create a new map and fill it with walls
        self.create_new_map(dimensions)
        self.fill_with_wall()

        for x in range(dimensions.x):
            for y in range(dimensions.y):
                self.new_map.set_tile(Vector(x, y), FLOOR)

    # ROGUE GENERATION
    def generate_rogue_level(self, dimensions, cols=3, rows=3):
        # Create a new map and fill it with walls
        self.create_new_map(dimensions)
        self.fill_with_wall()

        # Calculate the map dimensions of each grid cell and initalize a room grid with empty rooms
        self.grid_cell_dimensions = Vector(int(dimensions.x/cols), int(dimensions.y/rows))

        self.room_grid = RoomGrid(Vector(cols, rows))
        
        self.room_cols = cols
        self.room_rows = rows

        # Create a random room for each point
        for x in range(cols):
            for y in range(rows):
                point = Vector(x, y)
                
                pivot = self.get_rogue_room_pivot(point)
                dims = self.get_rogue_room_dim()
                
                new_room = Room(pivot, dims)

                self.room_grid.set_room(point, new_room)

        # Determine the prime path, a list of room points that should be followed
        points = self.determine_prime_path(Vector(0, 0))

        for p in points:
            self.apply_room(self.room_grid.get_room(p))

        return

        # Generate connections list


        # Determine room connections
        for i in range(len(points)):
            if (i+1) in range(len(points)):
                points[i].connect(points[i+1])
            if (i-1) in range(len(points)):
                points[i].connect(points[i-1])

        # Apply rooms
        for p in points:
            self.apply_room(self.room_grid[p.x, p.y])

        # Draw tunnels
        for x in range(cols):
            for y in range(rows):
                room1 = self.room_grid[x, y]
                for c in room1.connected_rooms:
                    self.tunnel_between_rooms(room1, c)

    def tunnel_between_rooms(self, room1, room2):
        r1x = 0
        r1y = 0
        r2x = 0
        r2y = 0
        if room1.pivot.x > room2.pivot.x: # Room 1 is right
            r1x = room1.pivot.x
            r1y = random.randint(room1.pivot.y + 1, room1.pivot.y + room1.dimensions.y + 1)

            r2x = room2.pivot.x + room2.dimensions.x
            r2y = random.randint(room2.pivot.y + 1, room2.pivot.y + room2.dimensions.y + 1)
        elif room1.pivot.x < room2.pivot.x: # Left
            r1x = room1.pivot.x + room1.dimensions.x
            r1y = random.randint(room1.pivot.y + 1, room1.pivot.y + room1.dimensions.y + 1)

            r2x = room2.pivot.x
            r2y = random.randint(room2.pivot.y + 1, room2.pivot.y + room2.dimensions.y + 1)

        elif room1.pivot.y > room2.pivot.y: # Room 1 is down
            r1y = room1.pivot.y
            r1x = random.randint(room1.pivot.x + 1, room1.pivot.x + room1.dimensions.x + 1)
        elif room1.pivot.y < room2.pivot.y: # Up
            pass

        d1 = Vector(r1x, r1y)
        d2 = Vector(r2x, r2y)

        distances = Vector(abs(d2.x - d1.x), abs(d2.y - d1.y))

        if d1.y < d2.y: # Tunnel up
            pass
        elif d1:
            pass

    def is_room_in_range(self, room_point):
        return (room_point.x >= 0 and room_point.x < self.room_cols) and (room_point.y >= 0 and room_point.y < self.room_rows)

    def get_rogue_room_pivot(self, point=Vector()):
        x = point.x * self.grid_cell_dimensions.x + 1
        y = point.y * self.grid_cell_dimensions.y
        return Vector(int(x), int(y))
    def get_rogue_room_dim(self):
        x = random.randint(4, self.grid_cell_dimensions.x - 1)
        y = random.randint(4, self.grid_cell_dimensions.y - 1)
        return Vector(x, y)
    
    # RECURSIVE ALGORITHM FOR DETERMINING A VIABLE PRIME PATH
    def determine_prime_path(self, point=Vector(), points=[]):
        points.append(point) # Add the current point to the list path

        options = [Vector(0,-1), Vector(0,1), Vector(1,0)] # Inital options - no left as that would go back

        while len(options) > 0: # If not all options are used up
            option = options.pop(random.randint(0, len(options) - 1)) # Remove a random option
            new_point = point + option

            # Room must be in range and room must not have already been accessed
            if self.is_room_in_range(new_point):
                if not new_point in points:
                    return self.determine_prime_path(new_point, points) # Move
        return points # No more possible moves, return final path
        
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
        self.distance_map = np.zeros(self.new_map.dimensions.get_tuple(), dtype=int)
        self.distance_map.fill(-1) # Initalize all distances to -1 - uninitalized
        sys.setrecursionlimit(self.new_map.dimensions.x * self.new_map.dimensions.y)
        self.flood_fill(Vector(1, 1), 0)

    def get_distance_map(self):
        return self.distance_map

    # RECURSIVE FLOOD FILL, DOES NOT WORK ON LARGER MAPS DUE TO PYTHON'S RECURSION LIMIT UNLESS USING sys.setrecursionlimit
    # Performs a flood fill operation starting at a point recursively and saves the resulting map to distance_map
    def flood_fill(self, point=Vector(0,0), distance=0):
        if not self.new_map.is_in_range(point): # Out of range, cease filling
            return
        if self.distance_map[point.x, point.y] != -1 and self.distance_map[point.x, point.y] <= distance: # Already filled with smaller value
            return
        if self.new_map.get_tile(point) != FLOOR: # Hit wall, terminate
            return

        # FLOOD FILLING
        self.distance_map[point.x, point.y] = distance
        new_distance = distance + 1
        directions = [Vector(1,0), Vector(-1,0), Vector(0,1), Vector(0,-1)]
        for d in directions:
            self.flood_fill(point + d, new_distance)
        return 
