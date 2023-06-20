# LEVEL
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 6.19.2023 - Created file to move map and level data here

from utilities.math_utility import *

# All the information regarding a level
class Level(object):
    def __init__(self, tilemap=None, hero=None, entities=None, start=Vector(0,0), end=Vector(1,1)):
        self.tilemap = tilemap
        self.hero = hero
        self.entities = entities
        self.start = start
        self.end = end