# HERO SUBCLASS
# The player controlled actor
# MountainQuest
# Felix Liu

# Version History
# 6.7.2023 - created file, created hero subclass
# 6.20.2023 - added health change handler

from game.actors.actor import *

class Hero(Actor):
    def __init__(self, position=Vector(0,0), char="@", color=Color.DEFAULT_COLOR, energy=1, energy_gain=1, health=5, game=None):
        super().__init__(position, char, color, energy, energy_gain, health)
        self.game = game
    def get_action(self):
        return super().get_action()

    # Collision handler - override
    def collide(self, other):
        super().collide(other)
    
    # Health handler - override
    def on_health_changed(self):
        super().on_health_changed()
        if self.health <= 0:
            print("\nGame over!") # Temporary game over
            self.game.stop()
            