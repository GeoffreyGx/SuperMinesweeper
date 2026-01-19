import pygame
import os
import dotenv
from scene import Scene
from elements.UI import Button
import scenes.shared

dotenv.load_dotenv(".env")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class PauseMenu(Scene):
    def __init__(self, previous_scene: Scene):
        super().__init__()
        self.previous_scene = previous_scene

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 128))
        self.RESUME_BUTTON = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.33, 100, 50, "Resume")
        self.MENU_BUTTON = Button(SCREEN_WIDTH/2, SCREEN_HEIGHT*0.33+70, 100, 50, "Menu")


    def input(self, events, kb_input):
        for event in events:
            if self.RESUME_BUTTON.handle_event(event) == True:
                from .GameScreen import GameScreen
                self.switch(scenes.shared.gameScene)
            if self.MENU_BUTTON.handle_event(event) == True:
                from .MainMenu import MainMenu
                self.switch(MainMenu())

    def render(self, screen: pygame.Surface):
        self.previous_scene.render(screen)
        screen.blit(self.overlay, (0, 0))
        self.RESUME_BUTTON.draw(screen)
        self.MENU_BUTTON.draw(screen)