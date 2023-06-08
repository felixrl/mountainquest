# PLOT MODULE
# MountainQuest
# Felix Liu

# VERSION HISTORY
# 6.7.2023 - created file

import matplotlib.pyplot as plt

class Plotter(object):
    def __init__(self, x_data=[], y_data=[]):
        self.x_data = x_data
        self.y_data = y_data
    def plot(self):
        plt.plot(self.x_data, self.y_data, 'o')
        plt.show()