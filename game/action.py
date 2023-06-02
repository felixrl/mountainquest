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
        new_pos = actor.get_position() + self.dir
        if game.map.is_in_range(new_pos):
            if game.map.get_tile(new_pos) == 0:
                actor.set_position(new_pos)
