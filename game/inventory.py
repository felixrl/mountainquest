# INVENTORY
# MountainQuest
# Felix Liu

# Version History
# 6.14.2023 - File created

from enum import IntEnum

class ItemType(IntEnum):
    WOOD = 0
    STONE = 1
    GOLD = 2

class Inventory(object):
    def __init__(self):
        self.items = {}

    def add_item(self, item_type, amount):
        if item_type in self.items:
            self.items[item_type] += amount
        else:
            self.items[item_type] = amount