# UTILITY FOR SAVING/LOADING MAP DATA TO FILE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# Created 5/24/2023

# TODO
# Load
# Save
# Level editor
# Dedicated directory that reports all avaliable load options
# Prompt for save overwriting

# SEARCH FOR SAVED FILES
# SORT IN ALPHABETICAL ORDER

OBJECT_TYPES = { 0: "FLOOR", 1: "WALL" }

# When saving maps, objects are encoded into a text character and saved in-line on its appropriate row
# Every line is written, then a newline is created and the next row is parsed

class MapFileManager(object):
    def __init__(self):
        pass

    def load_map_from_file(self, path):
        file_handle = open(path, 'r')

    def save_map_to_file(self, path):
        file_handle = open(path, 'w')
    
    def list_avaliable_files(self, path):
        pass
