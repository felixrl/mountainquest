# MAIN GAME LOGIC
# Decoupled from rendering
# MountainQuest
# Felix Liu

# Version History
# 5.29.2023 - created file

from utilities.math_utility import *

class Game(object):
    def __init__(self, map):
        self.actors = []
        self.current_actor_index = 0

        self.hero = None
        self.map = map

    # GAME LOOP
    # From https://journal.stuffwithstuff.com/2014/07/15/a-turn-based-game-loop/
    # For a decoupled game loop with control via the UI, process one actor at a time before returning control
    def process(self):
        if len(self.actors) > 0: # If there are actual actors
            action = self.actors[self.current_actor_index].get_action() # Get action

            if action == None:
                return

            action.perform(self.actors[self.current_actor_index], self) # Perform the action
            self.current_actor_index = (self.current_actor_index + 1) % len(self.actors) # Next actor

    # ACTORS
    def add_actor(self, a):
        self.actors.append(a)
    def remove_actor(self, a):
        self.actors.remove(a)
    
    def set_hero(self, a):
        self.hero = a
            
    # Playing controls
    def play(self):
        self.is_playing = True
    def stop(self):
        self.is_playing = False