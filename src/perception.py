# src/perception.py
class Perception:
    def __init__(self, environment):
        self.env = environment

    def sense(self, x, y):
        return self.env.get_water_quality(x, y)
