# KEYBOARD INPUT MANAGEMENT
# MountainQuest
# Felix Liu

# Version History
# 5.30.2023 - File created

from enum import IntEnum

class KeyCode(IntEnum):
    Q = 113
    S = 115
    LeftArrow = -203
    UpArrow = -204
    RightArrow = -205
    DownArrow = -206

def get_key_code(s):
    return ord(s)