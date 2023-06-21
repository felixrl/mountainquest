# INVENTORY
# MountainQuest
# Felix Liu

# Version History
# 6.14.2023 - File created
# 6.20.2023 - Added get and consume item methods, adjusted ItemTypes

from enum import IntEnum

class ItemType(IntEnum):
    POTION = 0
    POTION_MATERIAL = 1
    COIN = 2

# Strings for user-friendly representation
ITEM_NAMES = {
    ItemType.POTION: "Potion",
    ItemType.POTION_MATERIAL: "Ingredient",
    ItemType.COIN: "Coin"
}

class Inventory(object):
    def __init__(self):
        self.items = {}
    def __str__(self): # Stringify for UI printout
        final_str = ""
        for item in self.items:
            final_str = final_str + "{0}: {1} | ".format(ITEM_NAMES[item], self.items[item])
        return final_str

    # ADD ITEM, AMOUNT
    def add_item(self, item_type, amount):
        if item_type in self.items:
            self.items[item_type] += amount
        else:
            self.items[item_type] = amount

    # GET ITEM AMOUNT
    def get_item(self, item_type):
        if item_type in self.items: # Item inside inventory
            return self.items[item_type] 
        return 0 # None, return 0

    # CONSUME ITEM IF POSSIBLE, ELSE RETURN FALSE
    def consume_item(self, item_type, amount):
        if item_type in self.items:
            if self.get_item(item_type) >= amount: # Enough to consume
                self.items[item_type] -= amount
                return True
        return False
