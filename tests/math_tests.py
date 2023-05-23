# MATH TESTS
# MountainQuest
# Felix Liu

# python -m tests.math_tests

from utilities.math_utility import *

v1 = Vector(1, 1)
v2 = Vector(2, 2)
v3 = Vector(-1, -2)

assert v1 + v2 == Vector(3, 3)
v1 += v2
assert v1 == Vector(3, 3)

assert v3 + v2 == Vector(1, 0)

assert v3 - v2 == Vector(-3, -4)

assert v3 * 3 == Vector(-3, -6)

v1 -= v2
assert v1 == Vector(1, 1)

v1 *= v3
assert v1 == v3 
v1 *= v3
assert v1 == Vector(1, 4)

assert v1 / 2== Vector(0.5, 2)

print("All good!")