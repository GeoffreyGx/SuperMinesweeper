import pygame
from scene import Scene
from elements.UI import *
import logging
import os

logger = logging.getLogger(__name__)

class SettingsMenu(Scene):
    def __init__(self):
        super().__init__()
        logger.info("Settings Menu is loading...")
        self.tabs = [('graphics', BasicButton(110, 70, "Graphics")), ('sounds', BasicButton(110, 70+48+10, "Sounds")), ('multiplayer', BasicButton(110, 70+48*2+10*2, "Multiplayer"))]
        self.active_tab = self.tabs[0][0]
        
        self.graphics_tab = [('fullscreen_label', Label(250, 60, "Fullscreen")), ('fullscreen_enable', BasicButton(500, 70,"ON", action="fullscreen_on")), ('fullscreen_enable', BasicButton(650, 70,"OFF", action='fullscreen_off'))]
        self.sounds_tab = []
        self.multiplayer_tab = []

    def input(self, events, kb_input):
        for event in events:
            for button in self.tabs:
                if button[1].handle_event(event):
                    self.active_tab = button[0]
                    logger.error("Button %s has been clicked", button[0])
            for button in self.graphics_tab:
                if isinstance(button, tuple) and len(button) == 2:
                    key, widget = button
                    if hasattr(widget, 'handle_event') and widget.handle_event(event):
                        action = widget.getAction() if hasattr(widget, 'getAction') else None
                        if action == "fullscreen_on":
                            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        if action == "fullscreen_off":
                            pygame.display.set_mode((int(str(os.getenv("SCREEN_WIDTH"))), int(str(os.getenv("SCREEN_HEIGHT")))))


        if kb_input[pygame.K_ESCAPE]:
            from .MainMenu import MainMenu
            self.switch(MainMenu())

    def render(self, screen: pygame.Surface):
        screen.fill("#098098")
        for button in self.tabs:
            button[1].draw(screen)
        if self.active_tab == 'graphics':
            for button in self.graphics_tab:
                button[1].draw(screen)
        if self.active_tab == 'sounds':
            for button in self.sounds_tab:
                button[1].draw(screen)
        if self.active_tab == 'multiplayer':
            for button in self.multiplayer_tab:
                button[1].draw(screen)
