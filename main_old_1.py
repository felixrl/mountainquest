# MAIN PROGRAM - RUN THIS ONE
# MountainQuest
# Felix Liu

from asciimatics.screen import Screen

import time
import random
import logging

from utilities.math_utility import *

from game.game_object import *
from game.renderer import *
from game.timer import *

from game.map import *
from game.map_generator import *

MAP_DIMENSIONS = Vector(80, 24)
# MAP_DIMENSIONS = Vector(10, 10)

# Body component for physics processing
class Body(Component):
    def __init__(self, transform=None):
        super(Body, self).__init__()
        self.transform = transform
    def move_to(self, position=Vector(0,0)):
        if map.is_in_range(position):
            if map.is_floor(position):
                self.transform.position = position
    def move_by(self, direction=Vector(0,0)):
        new_position = self.transform.position + direction
        self.move_to(new_position)
    
    def start(self):
        return super().start()
    def update(self, delta):
        if not map.is_floor(self.transform.position):
            pass
            # print("Dead!")

class Player(GameObject):
    def __init__(self, position):
        super(Player, self).__init__(position)

        self.body = Body(self.transform)
        self.add_component(self.body)
        renderer = Renderer(self.transform, "@", WHITE)
        self.add_component(renderer)
class Enemy(GameObject):
    def __init__(self, position):
        super(Enemy, self).__init__(position)
        
        self.body = Body(self.transform)
        self.add_component(self.body)
        renderer = Renderer(self.transform, "*", RED)
        self.add_component(renderer)
        timer = Timer(0.2)
        timer.subscribe(self)
        self.add_component(timer)

    def on_timer(self, timer):
        dir = random.randint(0, 1)
        amount = random.randint(0, 1)
        new_direction_vector = Vector()
        if dir == 0:
            if amount == 0:
                new_direction_vector = Vector(1, 0)
            else:
                new_direction_vector = Vector(-1, 0)
        else:
            if amount == 0:
                new_direction_vector = Vector(0, 1)
            else:
                new_direction_vector = Vector(0, -1)
        self.body.move_by(new_direction_vector)





# MAP GENERATION
map_generator = MapGenerator(MAP_DIMENSIONS)
# map_generator.generate_dungeon_rooms(MAP_DIMENSIONS, 12)
# map_generator.generate_rogue_level(MAP_DIMENSIONS)
map_generator.create_dumb_map(MAP_DIMENSIONS)
map = map_generator.get_map()
map_generator.generate_distance_map()
distance_map = map_generator.get_distance_map()

# GAME OBJECT MANAGEMENT
game_objects = []
def add_game_object(game_object):
    game_objects.append(game_object)
def remove_game_object(game_object):
    game_objects.remove(game_object)

highest_point = (0, 0) # Point vector and distance value
player = Player(Vector(0, 0))
for x in range(map.dimensions.x):
    for y in range(map.dimensions.y):
        d = distance_map[x, y]
        if d == 0:
            player.transform.set_position(Vector(x, y))
        if highest_point[1] < d:
            highest_point = (Vector(x, y), d)
add_game_object(player)

finish_point = highest_point[0]

for i in range(random.randint(3, 10)):
    new_enemy = Enemy(Vector(random.randint(0, map.width - 1), random.randint(0, map.height - 1)))
    add_game_object(new_enemy)

# WATER TEST

class Water(GameObject):
    def __init__(self, position):
        super(Water, self).__init__(position)
        
        renderer = AnimatedRenderer(self.transform, ProceduralAnimation("animations/water.txt"), 12)
        self.add_component(renderer)

for x in range(20,40):
    for y in range(10, 20):
        pass
        # new_water = Water(Vector(x, y))
        # add_game_object(new_water)

def handle_input(e, screen):
    global player
    if e != None and hasattr(e, "key_code"):
        k = e.key_code
        match k:
            case -204: # up
                player.body.move_by(Vector(0, -1))
            case -203: # left
                player.body.move_by(Vector(-1, 0))
            case -206: # down
                player.body.move_by(Vector(0, 1))
            case -205: # right
                player.body.move_by(Vector(1, 0))





# GAME
PLAYING = 0
GAME_OVER = 1
VICTORY = 2

def start():
    # print(game_objects)
    for g in game_objects:
        g.start()
def update(delta):
    for g in game_objects:
        g.update(delta)
def render(screen):
    for g in game_objects:
        g.render(screen)

def game(screen):
    state = PLAYING
    previous_frame_time = time.time()
    cur_time = 0
    
    start()

    while True:
        # INPUT HANDLING
        e = screen.get_event()
        if e != None and hasattr(e, "key_code"):
            if e.key_code == 113: # Q to exit
                break
            if e.key_code == ord(" "):
                state = PLAYING
            # screen.print_at(e.key_code, 100, 10)
        handle_input(e, screen)

        # GAMEPLAY
        # Delta time
        delta_time = time.time() - previous_frame_time
        previous_frame_time = time.time()
        cur_time += delta_time

        update(delta_time)

        # RENDERING
        match state:
            case 0:
                for x in range(map.width):
                    for y in range(map.height):
                        c = "?"
                        match map.get_tile(Vector(x, y)):
                            case 0:
                                c = "."
                            case 1:
                                c = " "
                        screen.print_at(c, x, y, colour=WHITE)
                        if Vector(x, y) == finish_point:
                            screen.print_at("$", x, y, colour=YELLOW)
                        # screen.print_at(distance_map[x, y], x, y, colour=WHITE)
                render(screen)
            case 1:
                screen.print_at("GAME OVER", 16, 8)
        screen.print_at("*", 0, 0)
        screen.print_at("*", map.width, map.height)
        screen.refresh()

def main():
    print("Starting MountainQuest...")
    Screen.wrapper(game)
    print("Done!")
    return 0
main()