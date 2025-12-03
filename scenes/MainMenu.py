from scene import *
from elements.UI import Button
import logging
import pygame
logger = logging.getLogger(__name__)

class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        self.SINGLEPLAYER_BUTTON = Button(123, 200, 150, 50, "Singleplayer")
        self.MULTIPLAYER_BUTTON = Button(123, 200+50+10, 150, 50, "Multiplayer")
        self.SETTINGS_BUTTON = Button(123, 200+50*2+10*2, 150, 50, "Settingsplayer")
        self.QUIT_BUTTON = Button(123, 200+50*3+10*3, 150, 50, "Quit Game")

    def input(self, events, kb_input):
        for event in events:
            if self.SINGLEPLAYER_BUTTON.handle_event(event) == True:
                from .GameScreen import GameScreen
                self.switch(GameScreen())
            if self.MULTIPLAYER_BUTTON.handle_event(event) == True:
                logger.debug("Multiplayer button has been pressed")
            if self.SETTINGS_BUTTON.handle_event(event) == True:
                from .SettingsMenu import SettingsMenu
                self.switch(SettingsMenu())
            if self.QUIT_BUTTON.handle_event(event) == True:
                raise SystemExit

    def render(self, screen):
        screen.fill('#838283')
        self.SINGLEPLAYER_BUTTON.draw(screen)
        self.MULTIPLAYER_BUTTON.draw(screen)
        self.SETTINGS_BUTTON.draw(screen)
        self.QUIT_BUTTON.draw(screen)
        

        