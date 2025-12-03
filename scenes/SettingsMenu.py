import pygame
from scene import Scene
from elements.UI import *
import logging

logger = logging.getLogger(__name__)

class SettingsMenu(Scene):
    def __init__(self):
        super().__init__()
        logger.info("Settings Menu is loading...")
        self.tabs = [('graphics', BasicButton(110, 70, "Graphics")), ('sounds', BasicButton(110, 70+48+10, "Sounds")), ('multiplayer', BasicButton(110, 70+48*2+10*2, "Multiplayer"))]
        self.active_tab = self.tabs[0][0]
        
        self.graphics_tab = []

    def input(self, events, kb_input):
        for event in events:
            for button in self.tabs:
                if button[1].handle_event(event) == True:
                    self.active_tab = button[0]
                    logger.error("Button %s has been clicked", button[0])
        if kb_input[pygame.K_ESCAPE]:
            from .MainMenu import MainMenu
            self.switch(MainMenu())

    def render(self, screen: pygame.Surface):
        screen.fill("#098098")
        for button in self.tabs:
            button[1].draw(screen)
        if self.active_tab == 'graphics':

