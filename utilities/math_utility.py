# GAME MATH MODULE
# MountainQuest
# Felix Liu

import math

# A 2D vector class for directions, points, and positions
class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    # Mathematical operations
    def __eq__(self, value):
        return (self.x == value.x) and (self.y == value.y)
    def __add__(self, value):
        return self.add(value)
    def __iadd__(self, value):
        return self.add(value)
    def __sub__(self, value):
        return self.add(value.negative())
    def __isub__(self, value):
        return self.add(value.negative())
    def __mul__(self, value):
        return self.multiply(value)
    def __imul__(self, value):
        return self.multiply(value)
    def __truediv__(self, value):
        return self.multiply(1/value)
    def __itruediv__(self, value):
        return self.multiply(1/value)
    def __floordiv__(self, value):
        return self.multiply(1/value)
    def __ifloordiv__(self, value):
        return self.multiply(1/value)
    
    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def add(self, value):
        if type(value) == type(Vector()):
            return Vector(self.x + value.x, self.y + value.y)
        raise Exception("Invalid vector addition")
    def multiply(self, value):
        if type(value) == type(1) or type(value) == type(1.0):
            return Vector(self.x * value, self.y * value)
        elif type(value) == type(Vector()):
            return Vector(self.x * value.x, self.y * value.y)
        raise Exception("Invalid vector multiplication")

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)
    def normalized(self):
        return Vector(self.x / self.magnitude(), self.y / self.magnitude())
    def negative(self):
        return Vector(-self.x, -self.y)
    
    def get_tuple(self):
        return (self.x, self.y)
        