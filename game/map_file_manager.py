# UTILITY FOR SAVING/LOADING MAP DATA TO FILE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# Created 5/24/2023
# Added saving, loading, and listing functionality - 6/5/2023
# Fixed an issue where a loaded map would include an extra column on the far right - 6/6/2023

# TODO
# Level editor
# Dedicated directory that reports all avaliable load options
# Prompt for save overwriting
# ENCODING/DECODING SYSTEM MAP
# Make sure to check if directories exist before saving to path!

# SEARCH FOR SAVED FILES
# SORT IN ALPHABETICAL ORDER

from utilities.math_utility import *
from utilities.sort_utility import *

from game.map import *

from os import listdir
from os.path import isfile, join

OBJECT_TYPES = { 0: "0", 1: "1" }

# When saving maps, objects are encoded into a text character and saved in-line on its appropriate row
# Every line is written, then a newline is created and the next row is parsed

class MapFileManager(object):
    def __init__(self):
        pass

    def load_map_from_file(self, path):
        file_handle = open(path, 'r')

        lines = file_handle.readlines()

        # Get dimensions
        y_val = 0
        for l in lines:
            y_val += 1
        x_val = 0
        for c in lines[0].strip():
            x_val += 1
        dims = Vector(x_val, y_val)

        # Create map
        map = Map(dims)

        # Craft the map out of tiles
        x = 0
        y = 0
        for line in lines:
            x = 0
            processed_line = line.strip()
            for c in processed_line:
                pos = Vector(x, y)
                # print(pos)
                map.set_tile(pos, int(c))
                x += 1
            y += 1
        
        return map

    def save_map_to_file(self, path, map):
        file_handle = open(path, 'w')

        # data
        # WRITING ALWAYS HEIGHT, THEN WIDTH, SO FILE IS HUMAN-READABLE
        for y in range(map.height):
            for x in range(map.width):
                point = Vector(x, y)
                file_handle.write(OBJECT_TYPES[map.get_tile(point)])
            file_handle.write("\n")
        file_handle.close()
    
    def list_avaliable_files(self):  
        my_files = [f for f in listdir("maps") if isfile(join("maps", f))]
        return my_files

    def list_sorted_avaliable_files(self):
        avaliable_files = self.list_avaliable_files()
        return merge_sort(avaliable_files, compare_alphabetically)
