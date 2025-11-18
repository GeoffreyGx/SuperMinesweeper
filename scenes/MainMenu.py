from scene import *
from .GameScreen import *
from elements.UI import BasicButton
import logging
import pygame
logger = logging.getLogger(__name__)

class MainMenu(Scene):
    def input(self, events, kb_input):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.switch(GameScreen())

    def render(self, screen):
        screen.fill('#838283')

        

        