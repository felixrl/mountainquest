# ACTOR BASE CLASS
# Entities like player, enemy, etc
# MountainQuest
# Felix Liu

# Version History
# 5.29.2023 - created file

from utilities.math_utility import *

from game.action import *

class Actor(object):
    def __init__(self, position=Vector(0, 0), char="#"):
        self.position = position
        self.char = char

        # Action system
        self.next_action = None

    def update(self):
        pass
        # print("updating!")

    # Action system
    def get_action(self):
        selected_action = self.next_action
        self.next_action = None
        return selected_action
    def set_next_action(self, action=None):
        if action == None:
            return
        self.next_action = action

    def get_char(self):
        return self.char
    def get_position(self):
        return self.position
    def set_position(self, new_position=Vector(0,0)):
        self.position = new_position
    
class Enemy(Actor):
    def get_action(self):
        return MoveAction(Vector(0,1))
