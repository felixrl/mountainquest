# MAP
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.23.2023 - Began work on room connection system, prime path finder
# 5.25.2023 - Added demo map generator for full room, recursive function for generating a distance map with flood fill
# 6.1.2023 - Added function for creating a wall block
# 6.8.2023, 6.9.2023 - Added rogue tunneling functionality
# 6.12.2023 - Added entrance tile and exit tile

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

    # Functions for getting particular points
    def get_top_left(self):
        return self.pivot
    def get_top_right(self):
        return self.pivot + Vector(self.dimensions.x, 0)
    def get_bottom_left(self):
        return self.pivot + Vector(0, self.dimensions.y)
    def get_bottom_right(self):
        return self.pivot + self.dimensions

# A class defining a grid of rooms
class RoomGrid:
    def __init__(self, dimensions=Vector(3,3)):
        self.room_grid = np.zeros(dimensions.get_tuple(), dtype=Room)
        self.room_cols = dimensions.x
        self.room_rows = dimensions.y
    
    def set_room(self, point, room):
        self.room_grid[point.x, point.y] = room
    def get_room(self, point):
        return self.room_grid[point.x, point.y]

    def scalar_index_to_2d(self, i):
        x = i % self.room_cols
        y = i // self.room_rows
        return Vector(x, y)
    def point_to_scalar_index(self, point):
        return point.x + point.y * self.room_cols
    def get_at_scalar_index(self, i):
        point = self.scalar_index_to_2d(i)
        return self.room_grid[point.x, point.y]
    def get_modulus(self):
        return len(self.room_grid[0])


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
                offset = self.get_rogue_room_offset(dims)
                
                new_room = Room(pivot + offset, dims)

                self.room_grid.set_room(point, new_room)

        # Determine the prime path, a list of room points that should be followed
        points = self.determine_prime_path(Vector(0, 0), [])

        for p in points:
            self.apply_room(self.room_grid.get_room(p))

        # Apply rooms
        for p in points:
            self.apply_room(self.room_grid.get_room(p))

        # Determine room connections, tunnel
        for i in range(len(points)):
            if (i+1) in range(len(points)):
                self.tunnel_between_rogue_rooms(self.room_grid.point_to_scalar_index(points[i]), self.room_grid.point_to_scalar_index(points[i+1]))

        # Get the top-left corner of the first room and set it as the ENTRANCE
        starting_tile = self.room_grid.get_room(Vector(0,0)).pivot
        self.new_map.set_tile(starting_tile, ENTRANCE)

        # FLOOD FILL - TAKES TIME, DETERMINE MAXIMAL DISTANCE
        self.generate_distance_map(starting_tile) # Blocking, takes time
        max_val = np.max(self.distance_map)
        coords = np.argwhere(self.distance_map == max_val) # https://stackoverflow.com/questions/27175400/how-to-find-the-index-of-a-value-in-2d-array-in-python
        self.new_map.set_tile(Vector(coords[0][0], coords[0][1]), EXIT) # Set the exit to the FURTHEST tile!

    def tunnel_between_rogue_rooms(self, ri1, ri2):
        if ri1 > ri2: # Swap indices if ri1 is greater, we need to always go right or down
            s_temp = ri1
            ri1 = ri2
            ri2 = s_temp
        
        # Get the actual room data
        r1 = self.room_grid.get_at_scalar_index(ri1)
        r2 = self.room_grid.get_at_scalar_index(ri2)

        door1 = Vector(0,0)
        door2 = Vector(0,0)
        distance = 0
        turn_distance = 0
        delta = 0
        delta_turn = 0
        turning_point = 0

        # HORIZONTAL
        if ri1 + 1 == ri2:
            door1 = Vector(r1.get_top_right().x, random.randint(r1.get_top_right().y + 1, r1.get_bottom_right().y - 1)) # Door 1, right wall, random Y
            door2 = Vector(r2.get_top_left().x, random.randint(r2.get_top_left().y + 1, r2.get_bottom_left().y - 1)) # Door 2, left wall, random Y
            # horizontal distance
            distance = abs(door2.x - door1.x)
            # vertical distance (to move on turn)
            turn_distance = abs(door2.y - door1.y)
            delta = Vector(1,0)
            delta_turn = Vector(0, 0)

            if door1.y < door2.y:
                # moving upwards as the second door is higher
                delta_turn = Vector(0, 1)
            else:
                # moving downwards or not at all as the second door is lower
                delta_turn = Vector(0, -1)
        # VERTICAL
        elif ri1 + self.room_grid.get_modulus() == ri2:
            door1 = Vector(random.randint(r1.get_bottom_left().x + 1, r1.get_bottom_right().x - 1), r1.get_bottom_right().y)
            door2 = Vector(random.randint(r2.get_top_left().x + 1, r2.get_top_right().x - 1), r2.get_top_right().y)

            distance = abs(door2.y - door1.y)
            turn_distance = abs(door2.x - door1.x)

            delta = Vector(0,1)
            delta_turn = Vector(0,0)

            if door1.x < door2.x:
                # moving right
                delta_turn = Vector(1,0)
            else:
                # moving left
                delta_turn = Vector(-1,0)

        turning_point = random.randint(1, distance) # turn at a random distance in between

        # TUNNEL ACCORDING TO SETTINGS
        # http://99.255.210.85/2019/06/03/rogue-level-generation.html
        cur_tunnel_point = door1
        self.new_map.set_tile(cur_tunnel_point, 0) # SET THE TILE AS EMPTY
        while distance > 0: # Still not at target
            cur_tunnel_point += delta # move according to delta
            self.new_map.set_tile(cur_tunnel_point, 0) # SET THE TILE AS EMPTY
            if distance == turning_point: # Turn move vertically
                while turn_distance > 0: # Not yet moved all vertically
                    cur_tunnel_point += delta_turn
                    self.new_map.set_tile(cur_tunnel_point, 0) # SET THE TILE AS EMPTY
                    turn_distance -= 1
            distance -= 1


    def is_room_in_range(self, room_point):
        return (room_point.x >= 0 and room_point.x < self.room_cols) and (room_point.y >= 0 and room_point.y < self.room_rows)

    def get_rogue_room_pivot(self, point=Vector()): # The static pivot from each rogue room is tiled from
        x = point.x * self.grid_cell_dimensions.x + 1
        y = point.y * self.grid_cell_dimensions.y
        return Vector(int(x), int(y))
    def get_rogue_room_offset(self, dim): # A random offset to be added to each rogue room
        x = random.randint(0, self.grid_cell_dimensions.x - dim.x - 1)
        y = random.randint(1, self.grid_cell_dimensions.y - dim.y - 1) # Y offset always starts at one to prevent top clipping
        return Vector(x, y)
    def get_rogue_room_dim(self): # A random dimension for each room within bounds
        x = random.randint(4, self.grid_cell_dimensions.x - 1)
        y = random.randint(4, self.grid_cell_dimensions.y - 2)
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
        self.flood_fill(start + Vector(1,1), 0) # Add Vector(1,1) fixes it, off by one error?

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
