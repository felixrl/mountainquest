# GAME STATE
# MountainQuest
# Felix Liu

# Version History
# 6/16/2023 - file created

class GameState(object):
    def __init__(self, map=None, hero=None, entities=[]):
        self.map = map
        self.hero = hero
        self.entities = entities