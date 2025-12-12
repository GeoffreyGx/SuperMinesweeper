import pygame

class Camera:
    def __init__(self):
        self.RELATIVE_X = 0.0
        self.RELATIVE_Y = 0.0
        self.velocityX = 0.0
        self.velocityY = 0.0
    
    def right(self, amount = 5.0):
        self.velocityX-=amount

    def left(self, amount = 5.0):
        self.velocityX+=amount

    def up(self, amount = 5.0):
        self.velocityY-=amount

    def down(self, amount = 5.0):
        self.velocityY+=amount
    
    def tick(self):
        self.RELATIVE_X += self.velocityX
        self.RELATIVE_Y += self.velocityY
        self.velocityX *= 0.8
        self.velocityY *= 0.8
        if -0.1 < self.velocityX < 0.1 and self.velocityX :
            self.velocityX = 0.0
        if -0.1 < self.velocityY < 0.1 and self.velocityY :
            self.velocityY = 0.0

    def vector(self, x, y):
        return pygame.Vector2(x + self.RELATIVE_X, y + self.RELATIVE_Y)
