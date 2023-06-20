# TIME MODULE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 6.20.2023 - file created, migrated DeltaTime and other time related functions

import time
from datetime import datetime

# General Time object for managing time-related things
class Time(object):
    def __init__(self): # Init with deltaTime information
        # Delta time setup
        self.previous_frame_time = time.time()
        self.cur_time = 0

    def get_timestamp_string(self): # Generate a timestamp string using datetime
        # Timestamping with https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime/
        cur_datetime = datetime.now() 
        timestamp = cur_datetime.strftime("%Y%m%d%H%M%S") # https://www.programiz.com/python-programming/datetime/strftime
        return str(timestamp)

    # RESET DELTATIME
    def reset_delta_time(self):
        # Make sure delta time starts with zero and that the previous frame is now
        self.delta_time = 0
        self.previous_frame_time = time.time()

    # CALL UPDATE EVERY FRAME TO KEEP TIME VALUES UP TO DATE
    def update(self):
        # Set deltaTime to difference
        self.delta_time = time.time() - self.previous_frame_time
        self.previous_frame_time = time.time()

        # Track current time
        self.cur_time += self.delta_time

    # Get time
    def get_time(self):
        return time.time()
    # Get deltaTime
    def get_delta_time(self):
        return self.delta_time
