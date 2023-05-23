# TIMER
# MountainQuest
# Felix Liu

from game.game_object import *

# Timer component for tracking events and managing time
class Timer(Component):
    def __init__(self, interval=None):
        super(Timer, self).__init__()
        self.time_elapsed = 0.0
        self.subscribers = []
        self.interval = interval

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)
    def notify(self):
        for s in self.subscribers:
            s.on_timer(self)
    
    def set_interval(self, interval):
        self.interval = interval

    def start(self):
        return super().start()
    def update(self, delta):
        super(Timer, self).update(delta)
        self.time_elapsed += delta
        if self.time_elapsed >= self.interval:
            self.notify()
            self.time_elapsed -= self.interval