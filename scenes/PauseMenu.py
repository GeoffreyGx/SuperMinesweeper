import pygame
from scene import Scene
from elements.UI import Button

class PauseMenu(Scene):
    def __init__(self):
        super().__init__()
        self.overlay = pygame.Surface(pygame.)
        self.BUTTON = Button(20, 20, 20, 20, "tkt")

    def render(self, screen: pygame.Surface):
        screen.fill("#313131")
        self.BUTTON.draw(screen)