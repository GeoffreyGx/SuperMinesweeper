import pygame

class Camera:
    def __init__(self, x = 0, y = 0):
        self.RELATIVE_X = x
        self.RELATIVE_Y = y
    
    def right(self, amount = 10):
        self.RELATIVE_X = self.RELATIVE_X - amount

    def left(self, amount = 10):
        self.RELATIVE_X = self.RELATIVE_X + amount

    def up(self, amount = 10):
        self.RELATIVE_Y = self.RELATIVE_Y - amount

    def down(self, amount = 10):
        self.RELATIVE_Y = self.RELATIVE_Y + amount