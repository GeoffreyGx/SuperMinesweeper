import pygame

class Camera:
    def __init__(self):
        self.RELATIVE_X = 0.0
        self.RELATIVE_Y = 0.0
    
    def right(self, amount = 10.0):
        self.RELATIVE_X = self.RELATIVE_X - amount

    def left(self, amount = 10.0):
        self.RELATIVE_X = self.RELATIVE_X + amount

    def up(self, amount = 10.0):
        self.RELATIVE_Y = self.RELATIVE_Y - amount

    def down(self, amount = 10.0):
        self.RELATIVE_Y = self.RELATIVE_Y + amount
    
    def vector(self, x, y):
        return pygame.Vector2(x + self.RELATIVE_X, y + self.RELATIVE_Y)
