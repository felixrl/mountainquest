# ACTOR BASE CLASS
# Entities like player, enemy, etc
# MountainQuest
# Felix Liu

# Version History
# 5.29.2023 - created file
# 5.31.2023 - added Enemy subclass, where action is determined based on player location, made default actor action only return next_action
# 6.2.2023 - moved Enemy subclass to its own file

from utilities.math_utility import *

from game.actions.action import *
from game.inventory import Inventory

from game.game_renderer import Color

class Actor(object):
    def __init__(self, position=Vector(0, 0), char="#", color=Color.DEFAULT_COLOR, energy=1, energy_gain=1, health=3):
        self.position = position
        self.char = char
        self.color = color
        self.energy = energy
        self.energy_gain = energy_gain

        self.health = health

        # Setup inventory
        self.inventory = Inventory()

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
    def get_color(self):
        return self.color
    def get_position(self):
        return self.position
    def set_position(self, new_position=Vector(0,0)):
        self.position = new_position

    # Collision handler - called when one character attempts to move into another
    def collide(self, other):
        pass

    # Heal handler - called when a heal action is used
    def heal(self, amount):
        self.health += amount
        self.on_health_changed()
    # Damage handler - called when one character attacks this one
    def damage(self, amount):
        self.health -= amount
        self.on_health_changed()

    # Handler for on health changed - implement in subclasses
    def on_health_changed(self):
        pass
