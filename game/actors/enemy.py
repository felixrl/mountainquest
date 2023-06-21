# ENEMY SUBCLASS
# Entities that are enemies
# MountainQuest
# Felix Liu

# Version History
# 6.2.2023 - created file and moved enemy subclass
# 6.20.2023 - added health change handler

from game.actors.actor import *
from game.inventory import ItemType

import random

class Enemy(Actor):
    def __init__(self, position=Vector(0,0), char="e", color=Color.DEFAULT_COLOR, energy=1, energy_gain=1, health=3, game=None):
        super().__init__(position, char, color, energy, energy_gain, health)
        self.game = game
    def get_action(self):
        y_distance = self.game.hero.position.y - self.position.y
        x_distance = self.game.hero.position.x - self.position.x
        
        # print("{0}, {1}".format(x_distance, y_distance))
        new_action = None

        if abs(y_distance) > abs(x_distance):
            # move y
            if y_distance > 0:
                new_action = MoveAction(Vector(0,1))
            else:
                new_action = MoveAction(Vector(0,-1))
        else:
            if x_distance > 0:
                new_action = MoveAction(Vector(1,0))
            else:
                new_action = MoveAction(Vector(-1, 0))
            # move x

        return new_action

    # Collision handler - override
    def collide(self, other):
        super().collide(other)
        # save what the most recent collider other was
        self.other = other
    
    # Health handler - override
    def on_health_changed(self):
        super().on_health_changed()
        if self.health <= 0: # ENEMY DIE
            self.game.remove_actor(self)
 
            if self.other == self.game.hero: # Player kill, add drops!
                num_of_potion_ingredients = random.randint(0, 2)
                self.game.hero.inventory.add_item(ItemType.POTION_MATERIAL, num_of_potion_ingredients) # ADD A NUMBER OF POTION INGREDIENTS
                num_of_coins = random.randint(1, 5)
                self.game.hero.inventory.add_item(ItemType.COIN, num_of_coins) # ADD A NUMBER OF COINS
