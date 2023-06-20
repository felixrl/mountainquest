# MAIN
# MountainQuest
# Felix Liu

from utilities.math_utility import *

from screen.curses_screen import *

MAP_DIMENSIONS = Vector(80, 24)

def handle_input(e):
    print("handling")

def main():
    i = CursesInputHandler(handle_input)
    c = CursesScreen(i)

    f = TextGraphic(".")

    g = GridGraphic(dims=MAP_DIMENSIONS)
    for x in range(MAP_DIMENSIONS.x):
        for y in range(MAP_DIMENSIONS.y):
            g.set_graphic(f, Vector(x, y))
    c.add_graphic(g)

    c.add_graphic(TextGraphic("a", Vector(0,0), Color.WHITE, Color.BLACK))
    c.add_graphic(TextGraphic("b", Vector(0,1)))
    c.add_graphic(TextGraphic("c", Vector(1,0)))
    while True:
        c.update()
        c.update_input()
        if not c.active:
            break

main()