# MAIN GAME LOGIC
# Decoupled from rendering
# MountainQuest
# Felix Liu

# Version History
# 5.29.2023 - created file, added Game class

from utilities.math_utility import *

class Game(object):
    def __init__(self, map):
        self.actors = []
        self.current_actor_index = 0

        self.hero = None
        self.map = map

        self.is_playing = True

    # GAME LOOP
    # From https://journal.stuffwithstuff.com/2014/07/15/a-turn-based-game-loop/
    # For a decoupled game loop with control via the UI, process one actor at a time before returning control
    def process(self):
        if len(self.actors) > 0: # If there are actual actors
            cur_actor = self.actors[self.current_actor_index]
            # print(cur_actor)
            
            if cur_actor.energy >= 1: # More than 1 or has 1 energy
                action = cur_actor.get_action() # Get action

                if action == None:
                    return

                action.perform(cur_actor, self) # Perform the action
                cur_actor.energy -= 1

            self.current_actor_index = (self.current_actor_index + 1) % len(self.actors) # Next actor
            cur_actor.energy += cur_actor.energy_gain

    # ACTORS
    # Actor management
    def add_actor(self, a):
        self.actors.append(a)
    def remove_actor(self, a):
        self.actors.remove(a)
    
    def set_hero(self, a):
        self.hero = a

    # SEARCH FOR ACTOR BY POSITION
    def search_for_actor_at(self, position=Vector(0,0)):
        for actor in self.actors: # Linear search
            if actor.position == position:
                return actor
        return None # Not found

    # Playing controls
    def play(self):
        self.is_playing = True
    def stop(self):
        self.is_playing = False