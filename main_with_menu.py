# MAIN PROGRAM - RUN THIS ONE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.31.2023 - added input handling for arrow keys
# 6.2.2023 - added TIME_BETWEEN_PROCESS, delays turns by a constant value to avoid instantaneous movements
# 6.9.2023 - added tracebook tracing for on errors
# 6.10.2023 - revamped rendering system

from utilities.math_utility import *

from screen.ascii_screen import *

SCREEN_DIMENSIONS = Vector(80, 24)

# SCREENS

class MainMenu(object):
    def __init__(self):
        print("hi")

def main_menu(screen_context):
    screen_context.clear()
    title = ASCIIText(0, "MOUNTAINQUEST", Vector(int(SCREEN_DIMENSIONS.x / 2 - len("MOUNTAINQUEST") / 2), int(SCREEN_DIMENSIONS.y / 4)), Color.WHITE)
    screen_context.add_graphic(title)
    screen_context.add_graphic(ASCIIBorder(char="#", dims=SCREEN_DIMENSIONS))
    while(True):
        screen_context.update()

# GAME PROGRAM
def main():
    print("")
    print("> Starting MountainQuest...") # Start the game
    print("")
    print("> MountainQuest")
    print("> (a turn-based ASCII roguelike)")
    print("> © 2023 felixrl")

    with ManagedScreen() as screen: # Create screen with screen context
        screen_context = ASCIIScreen(screen)
        main_menu(screen_context)

    main_menu() # Start at main menu
    
    print("")
    print("> Done!") # Game finished
    return 0
main()