# RENDERER AND VARIANTS
# MountainQuest
# Felix Liu

from game.game_object import *
from game.timer import *

import random

DEFAULT_COLOR = 7
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
PURPLE = 5
TEAL = 6
BLACK = 0
WHITE = 7

# Renderer component for character, color, and animation processing
class Renderer(Component):
    # COLOR
    # 0 - black
    # 1 - red
    # 2 - green
    # 3 - yellow
    # 4 - blue
    # 5 - purp
    # 6 - teal
    # 7 - default (white)
    def __init__(self, transform=None, char="?", color=7):
        super(Renderer, self).__init__()
        self.transform = transform
        self.char = char
        self.color = color

    def set_char(self, char):
        self.char = char
    def set_color(self, color):
        self.color = color
    def get_char(self):
        return self.char
    def get_color(self):
        return self.color
    
    def start(self):
        return super().start()
    def update(self, delta):
        return super().update(delta)
    def render(self, screen):
        super(Renderer, self).render(screen)
        screen.print_at(self.char, self.transform.position.x, self.transform.position.y, colour=self.color)

class AnimatedRenderer(Renderer):
    def __init__(self, transform=None, animation=None, fps=12):
        super(AnimatedRenderer, self).__init__(transform)
        self.animation = animation
        self.timer = Timer(float(1) / float(fps))
        self.timer.subscribe(self)
        self.cur_frame = 0

    def start(self):
        return super().start()
    def update(self, delta):
        super().update(delta)
        self.timer.update(delta)
    def render(self, screen):
        super().render(screen)
    
    def on_timer(self, timer):
        self.cur_frame += 1
        new_frame = self.animation.get_frame(self.cur_frame)
        self.set_char(new_frame.char)
        self.set_color(new_frame.color)

class Frame(object):
    def __init__(self, char=None, color=None):
        self.char = char
        self.color = color
    def __str__(self):
        return "{0} {1}".format(self.char, self.color)

class Animation(object):
    def __init__(self):
        self.frames = []
    def get_frame(self, frame_number):
        return self.frames[frame_number % len(self.frames)]
    def add_frame(self, frame):
        self.frames.append(frame)

class CharacterAnimation(Animation):
    def __init__(self):
        super().__init__()

class ProceduralAnimation(Animation):
    def __init__(self, source_file=None):
        super().__init__()
        self.load_from_file(source_file)
    
    def load_from_file(self, source_file):
        file_handle = open(source_file, 'r')
        for line in file_handle.readlines():
            properties = line.strip().split(" ")
            new_frame = Frame(str(properties[0]), int(properties[1]))
            self.add_frame(new_frame)
        file_handle.close()
    
    def get_frame(self, frame_number):
        return self.frames[random.randint(0, len(self.frames) - 1)]