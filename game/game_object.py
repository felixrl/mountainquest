# GAME OBJECT
# MountainQuest
# Felix Liu

from utilities.math_utility import *

# GameObject object for composition - every gameObject has a position
class GameObject(object):
    def __init__(self, position=Vector(0, 0)):
        self.components = []
        self.transform = Transform(position)
    def start(self):
        for c in self.components:
            c.start()
    def update(self, delta):
        for c in self.components:
            c.update(delta)
    def render(self, screen):
        for c in self.components:
            c.render(screen)
        
    # Adding and removing components
    def add_component(self, component):
        self.components.append(component)
    def __iadd__(self, component):
        self.add_component(component)
    def remove_component(self, component):
        self.components.remove(component)
    def __isub__(self, component):
        self.remove_component(component)

# Component class - every component has a start and update function
class Component(object):
    def __init__(self):
        pass
    def start(self):
        pass
    def update(self, delta):
        pass
    def render(self, screen):
        pass

# Transform class - the positional component
class Transform(Component):
    def __init__(self, position=Vector(0,0)):
        self.set_position(position)
    def set_position(self, position=Vector(0,0)):
        self.position = position
    def get_position(self):
        return self.position