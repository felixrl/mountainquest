# ACTION
# Actions that an entity can perform
# MountainQuest
# Felix Liu

# Version History
# 5.30.2023 - created file

from utilities.math_utility import *

# ACTION ENCAPSULATES A REQUEST IN AN OBJECT
# This way, actions can be treated like first-class objects
# An example of the Command design pattern
# http://gameprogrammingpatterns.com/command.html

# BASE ABSTRACT ACTION
class Action(object):
    def __init__(self):
        pass
    def perform(self):
        pass

# ACTION TO BE PERFORMED BY AN ACTOR
class ActorAction(Action):
    def __init__(self):
        super().__init__()
    def perform(self, actor=None, game=None):
        super().perform()
        if actor == None:
            raise Exception("No actor specified for an actor action!")
        if game == None:
            raise Exception("No game specified for an actor action!")

# Action to move an actor
class MoveAction(ActorAction):
    def __init__(self, dir=Vector(0,0)):
        super().__init__()
        self.dir = dir
    def perform(self, actor=None, game=None):
        super().perform(actor, game)

        # actually move
        move = True
        new_pos = actor.get_position() + self.dir
        if not game.map.is_in_range(new_pos): # Out of range, can't move
            return
        if game.map.get_tile(new_pos) == 1: # Is wall, can't move
            return
        actor_at_position = game.search_for_actor_at(new_pos)
        if actor_at_position != None: # Call collision if someone is there! (ATTACK)
            actor_at_position.collide(actor)
            actor.collide(actor_at_position)

            # Attack code, when moving into target
            attack_action = AttackAction(self.dir)
            attack_action.perform(actor, game)

            return

        actor.set_position(new_pos) # All checks passed, move the actor

# Action to attack a tile
class AttackAction(ActorAction):
    def __init__(self, dir=Vector(0,0)):
        super().__init__()
        self.dir = dir
    def perform(self, actor=None, game=None):
        super().perform(actor, game)

        # Attack!
        new_pos = actor.get_position() + self.dir
        target_actor = game.search_for_actor_at(new_pos)

        if not game.map.is_in_range(new_pos): # Out of range, can't attack
            return
        if game.map.get_tile(new_pos) == 1: # Is wall, can't attack
            return
        
        actor_at_position = game.search_for_actor_at(new_pos)
        if actor_at_position != None: # Attack!
            actor_at_position.damage(1)

# Action to heal from inventory
class HealAction(ActorAction):
    def __init__(self, item_type=None):
        super().__init__()
        self.item_type = item_type
    def perform(self, actor=None, game=None):
        super().perform(actor, game)

        # Heal
        hasConsumed = actor.inventory.consume_item(self.item_type, 1)
        if hasConsumed: # Item consumed, heal
            actor.heal(2)