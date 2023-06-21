# MAIN PROGRAM - RUN THIS ONE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.31.2023 - added input handling for arrow keys
# 6.2.2023 - added TIME_BETWEEN_PROCESS, delays turns by a constant value to avoid instantaneous movements
# 6.9.2023 - added tracebook tracing for on errors
# 6.12.2023 - added victory condition
# 6.20.2023 - finished majority rewrite, split entity decision making into TileMap and MapGenerator

from asciimatics.screen import Screen, ManagedScreen

from utilities.math_utility import *
from utilities.time_utility import Time
from utilities.color_utility import Color

from game.game import Game
from game.tilemap import TileType
from game.game_renderer import GameRenderer
from game.map_generator import MapGenerator
from game.actors.hero import Hero
from game.actors.enemy import Enemy
from game.actions.action import MoveAction, HealAction
from game.inventory import ItemType

from level_editor.map_file_manager import MapFileManager
from level_editor.editor import *

import game.input.keyboard as Keyboard



# https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
# for tracing errors
import traceback

MAP_DIMENSIONS = Vector(80, 24) # Dimensions of the map
TIME_BETWEEN_PROCESS = 0.05
MAP_FILE_MANAGER = MapFileManager()

TIME = Time()

def save_game(game):
    MAP_FILE_MANAGER.save_map_to_file("maps/map-{0}.txt".format(TIME.get_timestamp_string()), game.map)



# ---------------------
# GAME SESSION IN ASCII
# ---------------------

# INPUT HANDLER
def handle_game_input(game, e):
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
            case Keyboard.KeyCode.S: # SAVE FILE
                save_game(game)
            case Keyboard.KeyCode.Z: # HEAL
                game.hero.set_next_action(HealAction(ItemType.POTION))
            case Keyboard.KeyCode.Q: # QUIT
                return -1
# MAIN GAME
def game(screen, preload_map=None):
    try:
        # Get map
        map = preload_map
        if map == None: # No map, generate map
            map_generator = MapGenerator(MAP_DIMENSIONS) # Create a level generator
            map_generator.generate_rogue_level(MAP_DIMENSIONS)
            map = map_generator.get_new_tilemap()

        # Create game
        cur_game = Game(map)
        # Create renderer
        cur_game_renderer = GameRenderer(cur_game)

        # Create actors based on map spawners and initalize certain values
        exit_point = None
        for x in range(MAP_DIMENSIONS.x):
            for y in range(MAP_DIMENSIONS.y):
                if map.is_tile_type(Vector(x,y), TileType.ENTRANCE): # SPAWN THE PLAYER AT THE ENTRANCE
                    new_player = Hero(Vector(x,y), "@", Color.WHITE, game=cur_game, health=5)
                    cur_game.add_actor(new_player)  
                    cur_game.set_hero(new_player)

                    # Spawn with 1 potion, 2 ingredients
                    new_player.inventory.add_item(ItemType.POTION, 1)
                    new_player.inventory.add_item(ItemType.POTION_MATERIAL, 2)
                elif map.is_tile_type(Vector(x,y), TileType.ENEMY_SPAWNER): # SPAWN THE ENEMY AT ENEMY SPAWN POINTS
                    new_enemy = Enemy(Vector(x,y), "e", Color.RED, 1, 0.5, health=2, game=cur_game)
                    cur_game.add_actor(new_enemy)
                elif map.is_tile_type(Vector(x,y), TileType.EXIT): # ASSIGN THE EXIT POINT TO BE THE EXIT
                    exit_point = Vector(x,y)

        # SETUP PROCESS TIMER FOR TURN TICKS
        TIME.reset_delta_time()
        process_timer = TIME_BETWEEN_PROCESS

        while True: # GAME LOOP
            # DELTA TIME
            TIME.update()
            process_timer += TIME.get_delta_time() 

            # INPUT HANDLING
            e = screen.get_event()
            res = handle_game_input(cur_game, e) # Pass input handling
            if res == -1: # Input wants to quit! Quit the game
                break

            while process_timer >= TIME_BETWEEN_PROCESS:
                process_timer -= TIME_BETWEEN_PROCESS
                cur_game.process()

            if cur_game.hero.get_position() == exit_point:
                 print("\nYou win!")
                 cur_game.stop()
            
            if not cur_game.is_playing:
                break

            # RENDERING
            cur_game_renderer.render(screen)
            screen.refresh()    
    except Exception as e:
        print("\n> Error: " + str(e))
        print("> " + str(traceback.format_exc()))
        print("> An error occured in MountainQuest. Exiting to the main menu.")



# LEVEL EDITOR BROWSE MENU
def level_editor_menu():
    list_of_maps = MAP_FILE_MANAGER.list_avaliable_files() # Get avaliable map paths in /maps
    while True:
        print("")
        print("> LEVEL EDITOR (Enter q to exit)\n")
        for i in range(len(list_of_maps)): # Show the avaliable maps in print listing
            print("{0}. {1}".format(i + 1, list_of_maps[i]))
        if len(list_of_maps) < 1:
            print("No maps avaliable in maps. (Make one?)")
        print("")

        p_input = input("> ").strip().lower() # Player input, processed and standardized
        # INT PROCESSING
        try:
            i_input = int(p_input) # int value of the player's input
            with ManagedScreen() as screen:
                loaded_map = MAP_FILE_MANAGER.load_map_from_file("maps/" + list_of_maps[i_input - 1])
                level_editor(screen, loaded_map)
        except:
            # STRING PROCESSING
            match p_input:
                case "q":
                    break
                case "s": # SORTED PRINT
                    list_of_maps = MAP_FILE_MANAGER.list_sorted_avaliable_files() # Get avaliable map paths in /maps
                case "l": # NOT SORTED PRINT
                    list_of_maps = MAP_FILE_MANAGER.list_avaliable_files()
                case _:
                    print("\nPlease enter a valid input.")

# LEVEL EDITOR
def level_editor(screen, preload_map=None):
    try:
        # Get map
        map = preload_map

        # Create game
        cur_game = Game(map)
        # Create renderer
        cur_game_renderer = GameRenderer(cur_game)

        cursor_position = Vector(0,0)

        while True: # GAME LOOP
            # INPUT HANDLING
            e = screen.get_event()
            # res = handle_input(cur_game, e) # Pass input handling
            # if res == -1: # Input wants to quit! Quit the game
            #     break

            # RENDERING
            cur_game_renderer.render(screen)

            # MOUSE HANDLING
            if type(e) == type(MouseEvent(0,0, None)): # If it is a mouse event
                if e.x < MAP_DIMENSIONS.x and e.y < MAP_DIMENSIONS.y:
                    cursor_position = Vector(e.x, e.y)
            screen.print_at("█", cursor_position.x, cursor_position.y, Color.YELLOW) # Cursor
            
            screen.refresh()    
    except Exception as e:
        print("\n> Error: " + str(e))
        print("> " + str(traceback.format_exc()))
        print("> An error occured in the MountainQuest level editor. Exiting to the level browser.")



# MAIN MENU USING TYPICAL TERMINAL UI
# Instructions text includes newlines
main_menu_instructions = """
1 - play
2 - level editor
3 - quit
"""
def main_menu():
    while True:
        print(main_menu_instructions)
        p_input = input("> ").strip().lower() # Player input, processed and standardized
        # INT PROCESSING
        try:
            i_input = int(p_input) # int value of the player's input
            match i_input:
                case 1: # RUN GAME
                    with ManagedScreen() as screen: # using screen from ASCIImatics
                        game(screen)
                    print("\n> Exiting game...")
                case 2: # LEVEL EDITOR
                    level_editor_menu()
                    print("\n> Exiting level editor...")
                case 3: # QUIT
                    break 
                case _:
                    raise Exception("Invalid input.")
        except:
            # STRING PROCESSING
            match p_input:
                case "q": # QUIT
                    break
                case _:
                    print("\nPlease enter a valid input.")



# ------------
# MAIN PROGRAM
# ------------
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