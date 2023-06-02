# MAIN PROGRAM - RUN THIS ONE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.31.2023 - added input handling for arrow keys
# 6.2.2023 - added TIME_BETWEEN_PROCESS, delays turns by a constant value to avoid instantaneous movements

from asciimatics.screen import Screen
from utilities.math_utility import *

from game.game import *
from game.game_renderer import *
from game.map import *
from game.map_generator import *
from game.actor import *
from game.actors.enemy import *
from game.action import *

import game.input.keyboard as Keyboard

import time
import random
import logging



MAP_DIMENSIONS = Vector(80, 24) # Dimensions of the map
TIME_BETWEEN_PROCESS = 0.01

def start():
    pass
def update():
    pass
def render(screen):
    pass

# INPUT HANDLER
def handle_input(game, e):
    if e != None and hasattr(e, "key_code"):
        match e.key_code:
            # Movement inputs
            case Keyboard.KeyCode.UpArrow:
                game.hero.set_next_action(MoveAction(Vector(0,-1)))
            case Keyboard.KeyCode.DownArrow:
                game.hero.set_next_action(MoveAction(Vector(0,1)))
            case Keyboard.KeyCode.LeftArrow:
                game.hero.set_next_action(MoveAction(Vector(-1,0)))
            case Keyboard.KeyCode.RightArrow:
                game.hero.set_next_action(MoveAction(Vector(1,0)))
            case Keyboard.KeyCode.Q:
                return -1

# GAME SESSION IN ASCII
def game(screen):
    try:
        # Map generation
        map_generator = MapGenerator(MAP_DIMENSIONS)
        map_generator.create_dumb_map(MAP_DIMENSIONS)
        map_generator.generate_rogue_level(MAP_DIMENSIONS)
        #for i in range(2):
        #    pivot = Vector(random.randint(0, MAP_DIMENSIONS.x - 1), random.randint(0, MAP_DIMENSIONS.y - 1))
        #    size = Vector(random.randint(1, 32), random.randint(1, 32))
        #    map_generator.add_wall_block(pivot, size)
        
        map = map_generator.get_map()

        # Create game
        cur_game = Game(map)

        # Create renderer
        cur_game_renderer = GameRenderer(cur_game)

        # Create actors
        new_player = Actor(Vector(1, 1), "@", Color.WHITE)
        cur_game.add_actor(new_player)  
        cur_game.set_hero(new_player)

        for i in range(10):
            new_pos = Vector(0,0)
            while True:
                new_pos = Vector(random.randint(0, MAP_DIMENSIONS.x - 1), random.randint(0, MAP_DIMENSIONS.y - 1))
                if cur_game.map.get_tile(new_pos) == TileType.FLOOR:
                    break
            new_enemy = Enemy(new_pos, "e", Color.RED, 1, 0.5, cur_game)
            cur_game.add_actor(new_enemy)

        # for x in range(MAP_DIMENSIONS.x):
        #    for y in range(MAP_DIMENSIONS.y):
        #       if random.randint(0, 100) < 1:
        #            new_enemy = Enemy(Vector(x,y), "e")
        #            cur_game.add_actor(new_enemy)

        start() # STARTING GAME

        previous_frame_time = time.time()
        cur_time = 0
        process_timer = 0.0

        while True: # GAME LOOP
            # DELTA TIME
            delta_time = time.time() - previous_frame_time
            previous_frame_time = time.time()
            # Increment timers and trackers
            cur_time += delta_time
            process_timer += delta_time 

            # INPUT HANDLING
            e = screen.get_event()
            res = handle_input(cur_game, e) # Pass input handling
            if res == -1: # Input wants to quit! Quit the game
                break

            while process_timer >= TIME_BETWEEN_PROCESS:
                process_timer -= TIME_BETWEEN_PROCESS
                cur_game.process()

            # RENDERING
            cur_game_renderer.render(screen)
            screen.refresh()    
    except Exception as e:
        print("\n> Error: " + str(e))
        print("> An error occured in MountainQuest. Exiting to the main menu.")

# MAIN MENU
main_menu_instructions = """
1 - play
2 - level editor
3 - options
4 - credits
5 - quit
"""
# The above text has leading and trailing new lines included

# MAIN MENU USING TYPICAL TERMINAL UI
# Todo: create an ASCIImatics navigatable menu
def main_menu():
    # MAIN MENU LOOP
    while True:
        print(main_menu_instructions)
        p_input = input("> ").strip().lower() # Player input, processed and standardized
        # INT PROCESSING
        try:
            i_input = int(p_input) # int value of the player's input
            match i_input:
                case 1:
                    Screen.wrapper(game)
                    print("\n> Exiting game...")
                case 2:
                    print("\nlevel editor")
                case 3:
                    print("\noptions")
                case 4:
                    print("\ncredits")
                case 5:
                    break
                case _:
                    raise Exception("Invalid input.")
        except:
            # STRING PROCESSING
            match p_input:
                case "q":
                    break
                case _:
                    print("\nPlease enter a valid input.")

# GAME PROGRAM
def main():
    print("")
    print("> Starting MountainQuest...") # Start the game
    print("")
    print("> MountainQuest")
    print("> (a turn-based ASCII roguelike)")
    print("> © 2023 felixrl")
    main_menu() # Start at main menu
    print("")
    print("> Done!") # Game finished
    return 0
main()