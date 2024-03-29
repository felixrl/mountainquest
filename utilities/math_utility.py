# GAME MATH MODULE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 5.23.2023 - Added comments
# 6.1.2023 - Added interpolation

import math

# INTERPOLATION FUNCTIONS
# Linear interpolation
def lerp(start, end, t):
    return start * (1.0 - t) + end * t # Weighted 100% for start at 0.0 and 100% for end at 1.0

# A 2D vector class for directions, points, and positions
class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    # Mathematical operations
    # Addition and subtraction (subtraction uses inversion of second vector)
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
    
    # Multiplication
    def __mul__(self, value):
        return self.multiply(value)
    def __imul__(self, value):
        return self.multiply(value)
    
    # Division overrides, all use inverse multiplciation (1/value)
    # TODO: fix floor divisons, make sure to actually floor
    def __truediv__(self, value):
        return self.multiply(1/value)
    def __itruediv__(self, value):
        return self.multiply(1/value)
    def __floordiv__(self, value):
        return self.multiply(1/value)
    def __ifloordiv__(self, value):
        return self.multiply(1/value)
    
    def __str__(self): # Format and return string "(x, y)"
        return "({0}, {1})".format(self.x, self.y)

    def add(self, value): # Sum vectors
        if type(value) == type(Vector()): # Only vectors can be added to vectors (x+x1, y+y1)
            return Vector(self.x + value.x, self.y + value.y)
        raise Exception("Invalid vector addition")
    def multiply(self, value): # Multiply vectors
        if type(value) == type(1) or type(value) == type(1.0): # Floats and ints get scalar multiplication
            return Vector(self.x * value, self.y * value)
        elif type(value) == type(Vector()): # For the purposes of this implementation, vector by vector produces (x*x1, y*y1)
            return Vector(self.x * value.x, self.y * value.y)
        raise Exception("Invalid vector multiplication")

    def magnitude(self): # Returns the hypotenuse of the triangle made with x and y
        return math.sqrt(self.x**2 + self.y**2)
    def normalized(self): # Normalizes the vector to the range of -1 to 1 for x and y
        return Vector(self.x / self.magnitude(), self.y / self.magnitude())
    def negative(self): # Inverts both (x, y) to (-x, -y), multiplication by -1
        return Vector(-self.x, -self.y)
    def rounded(self): # Returns a vector rounded to the nearest integer points
        return Vector(round(self.x), round(self.y))
    
    def distance(self, target): # Returns the distance from self to target
        return self - target
    def diagonal_distance(self, target): # Returns the total number of tiles to fill a diagonal line
        return Vector(max(abs(self.distance(target).x)))

    def get_tuple(self): # Returns a tuple of (x, y)
        return (self.x, self.y)
    
    def lerp(self, target, t): # Linearly interpolate between this vector and the target vector
        if type(target) == type(Vector()):
            return Vector(lerp(self.x, target.x, t), lerp(self.y, target.y, t))
        raise Exception("Invalid vector linear interpolation")