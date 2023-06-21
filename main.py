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
from game.tilemap import TileType, TileMap
from game.game_renderer import GameRenderer
from game.map_generator import MapGenerator
from game.actors.hero import Hero
from game.actors.enemy import Enemy
from game.actions.action import MoveAction, HealAction, CraftAction
from game.inventory import ItemType

from level_editor.map_file_manager import MapFileManager
from level_editor.editor import *
from level_editor.editor_renderer import EditorRenderer

import game.input.keyboard as Keyboard

from enum import IntEnum



# https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
# for tracing errors
import traceback

MAP_DIMENSIONS = Vector(80, 24) # Dimensions of the map
TIME_BETWEEN_PROCESS = 0.01
MAP_FILE_MANAGER = MapFileManager()

TIME = Time()

# Save util function
def save_game(game):
    MAP_FILE_MANAGER.save_map_to_file("maps/" + get_time_file_name(), game.map)
def save_editor(editor, file_name=""):
    MAP_FILE_MANAGER.save_map_to_file(file_name, editor.map)
# Get file name for current time
def get_time_file_name():
    return "map-{0}.txt".format(TIME.get_timestamp_string())



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
            case Keyboard.KeyCode.X: # CRAFT
                game.hero.set_next_action(CraftAction(ItemType.POTION, ItemType.POTION_MATERIAL, 3))
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
                    new_enemy = Enemy(Vector(x,y), "e", Color.RED, 1, 0.5, health=1, game=cur_game)
                    cur_game.add_actor(new_enemy)
                elif map.is_tile_type(Vector(x,y), TileType.EXIT): # ASSIGN THE EXIT POINT TO BE THE EXIT
                    exit_point = Vector(x,y)
        
        # CHECK IF A PLAYER ACTUALLY EXISTS
        if cur_game.hero == None:
            print("> Game cannot start without player.")
            return
        # CHECK IF AN EXIT ACTUALLY EXISTS
        if type(exit_point) != type(Vector()):
            print("> Game cannot start without exit.")
            return

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

            # Game end - VICTORY
            if cur_game.hero.get_position() == exit_point:
                 print("\nYou win!")
                 print("Your score: {0} coins".format(cur_game.hero.inventory.get_item(ItemType.COIN)))
                 cur_game.stop()
            
            # End the game if it is stopped
            if not cur_game.is_playing:
                break

            # RENDERING
            cur_game_renderer.render(screen)
            screen.refresh()    
    except Exception as e:
        print("\n> Error: " + str(e))
        print("> " + str(traceback.format_exc()))
        print("> An error occured in MountainQuest. Exiting to the main menu.")



# LEVEL EDITOR
def level_editor(screen, preload_map=None, file_name=""):
    try:
        # Create game
        cur_editor = LevelEditor(preload_map)
        # Create renderer
        cur_editor_renderer = EditorRenderer(cur_editor)

        # Cursor
        cursor_position = Vector(0,0)

        while True: # GAME LOOP
            # INPUT HANDLING
            e = screen.get_event()
            # INPUT HANDLER
            if e != None and hasattr(e, "key_code"):

                # Tile switcher
                if e.key_code == ord("1"):
                    cur_editor.set_selected_tile(TileType.FLOOR)
                if e.key_code == ord("2"):
                    cur_editor.set_selected_tile(TileType.WALL)
                if e.key_code == ord("3"):
                    cur_editor.set_selected_tile(TileType.ENTRANCE)
                if e.key_code == ord("4"):
                    cur_editor.set_selected_tile(TileType.EXIT)
                if e.key_code == ord("5"):
                    cur_editor.set_selected_tile(TileType.ENEMY_SPAWNER)

                match e.key_code:
                    case Keyboard.KeyCode.G:
                        # Generate a template for this map
                        cur_map_generator = MapGenerator(MAP_DIMENSIONS)
                        cur_map_generator.generate_rogue_level(MAP_DIMENSIONS)
                        cur_editor.map = cur_map_generator.get_new_tilemap()
                    case Keyboard.KeyCode.P: # PLAY CURRENT
                        try:
                            game(screen, cur_editor.map)
                        except:
                            print("error")
                    case Keyboard.KeyCode.S: # SAVE
                        try:
                            save_editor(cur_editor, "maps/" + file_name)
                        except:
                            print("An error occurred while saving.")
                    case Keyboard.KeyCode.Q: # QUIT
                        break

            # RENDERING
            cur_editor_renderer.render(screen)

            # MOUSE HANDLING
            if type(e) == type(MouseEvent(0,0, None)): # If it is a mouse event
                if e.x < MAP_DIMENSIONS.x and e.y < MAP_DIMENSIONS.y: # In map range
                    cursor_position = Vector(e.x, e.y) # Set the cursor position
                    if e.buttons == MouseEvent.LEFT_CLICK: # PLACE
                        cur_editor.set_tile(cursor_position) # Set tile on click
                    elif e.buttons == MouseEvent.RIGHT_CLICK: # REMOVE
                        match cur_editor.get_tile(cursor_position):
                            case TileType.FLOOR:
                                cur_editor.map.set_tile(cursor_position, TileType.WALL)
                            case TileType.ENEMY_SPAWNER:
                                cur_editor.map.set_tile(cursor_position, TileType.FLOOR)
                            case _:
                                pass
            screen.print_at("▄", cursor_position.x, cursor_position.y, Color.YELLOW) # Cursor rendering
            
            screen.refresh()    
    except Exception as e:
        print("\n> Error: " + str(e))
        print("> " + str(traceback.format_exc()))
        print("> An error occured in the MountainQuest level editor. Exiting to the level browser.")



# LEVEL EDITOR BROWSE MENU
level_browser_instructions = """
[n] - open editor for map
play [n] - play map
rename [n] [name] - rename map (no spaces permitted)
delete [n] - delete map
new - create a new empty map
s - print maps in sorted alphabetical order
rs - print maps in reverse sorted alphabetical order
l - print maps in default file order
q - quit
"""

class BrowserState(IntEnum):
    DEFAULT = 0
    SORTED = 1
    REVERSE = 2

def level_editor_menu():
    level_state = BrowserState.DEFAULT
    while True:
        list_of_maps = MAP_FILE_MANAGER.list_avaliable_files() # Get avaliable map paths in /maps
        if level_state == BrowserState.SORTED:
            list_of_maps = MAP_FILE_MANAGER.list_sorted_avaliable_files()
        elif level_state == BrowserState.REVERSE:
            list_of_maps = MAP_FILE_MANAGER.list_sorted_avaliable_files()
            list_of_maps.reverse()
            
        print("")
        print("> LEVEL EDITOR")
        print(level_browser_instructions)
        print("> MAPS")

        for i in range(len(list_of_maps)): # Show the avaliable maps in print listing
            print("{0}. {1}".format(i + 1, list_of_maps[i]))
        if len(list_of_maps) < 1:
            print("No maps avaliable. (Make one?)")
        print("")

        p_input = input("> ").strip().lower() # Player input, processed and standardized
        # INT PROCESSING
        try:
            i_input = int(p_input) # int value of the player's input
            with ManagedScreen() as screen: # EDIT FILE
                loaded_map = MAP_FILE_MANAGER.load_map_from_file("maps/" + list_of_maps[i_input - 1])
                level_editor(screen, loaded_map, list_of_maps[i_input - 1])
        except:
            # STRING PROCESSING
            args = p_input.split(" ")
            cmd = args.pop(0)
            match cmd:
                case "new": # NEW FILE
                    with ManagedScreen() as screen:
                        new_map = TileMap(MAP_DIMENSIONS)
                        new_map.fill(TileType.WALL)
                        level_editor(screen, new_map, get_time_file_name())
                case "play": # PLAY FILE
                    num_arg = int(args[0])
                    with ManagedScreen() as screen:
                        loaded_map = MAP_FILE_MANAGER.load_map_from_file("maps/" + list_of_maps[num_arg - 1])
                        game(screen, loaded_map)
                case "delete": # DELETE FILE
                    num_arg = int(args[0])
                    MAP_FILE_MANAGER.delete_map("maps/" + list_of_maps[num_arg - 1])
                case "rename": # Rename file
                    try:
                        num_arg = int(args[0])
                        new_name = args[1]
                    
                        MAP_FILE_MANAGER.rename_map("maps/" + list_of_maps[num_arg -1], "maps/{0}.txt".format(new_name))
                    except:
                        print("\n> Rename failed. Please enter a valid name.")
                case "q":
                    break
                case "s": # SORTED PRINT
                    level_state = BrowserState.SORTED
                case "rs": # REVERSE SORT
                    level_state = BrowserState.REVERSE
                case "l": # NOT SORTED PRINT
                    level_state = BrowserState.DEFAULT
                case _:
                    print("\nPlease enter a valid input.")

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
    print("")
    print("MAKE SURE TO FULLSCREEN THE TERMINAL WINDOW")
    main_menu() # Start at main menu
    print("")
    print("> Done!") # Game finished
    return 0
main()