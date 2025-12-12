import logging
import pygame
import utils.camera
from scene import Scene
from elements.UI import ClickableAsset
import sweeper.world as sweeper_world

logger = logging.getLogger(__name__)

class GameScreen(Scene):
    camera = utils.camera.Camera()
    def __init__(self):
        super().__init__()
        self.PAUSE_BUTTON = ClickableAsset("pause_button", 30, 30, 30, 30)
        self.SAVE_BUTTON = ClickableAsset("save_button", 70, 30, 30, 30)
        self.HELP_BUTTON = ClickableAsset("help_button", 110, 30, 30, 30)
        self.world = sweeper_world.World(42)

    def update(self):
        self.previous_scene = self

    def input(self, events, kb_input):
        if kb_input[pygame.K_s]:
            self.camera.up()
        if kb_input[pygame.K_z]:
            self.camera.down()
        if kb_input[pygame.K_q]:
            self.camera.left()
        if kb_input[pygame.K_d]:
            self.camera.right()
        
        for event in events:
            if self.PAUSE_BUTTON.handle_event(event):
                from .PauseMenu import PauseMenu
                self.switch(PauseMenu(self.previous_scene))
                logger.debug("Pause Menu was invoked!")
            if self.world.handle_click_event(event)==True:
                mouseX, mouseY = event.pos
                camX, camY = self.camera.vector(0,0)
                self.world.uncoverAt(int(mouseX-camX)//32, int(mouseY-camY)//32)


    def render(self, screen):
        screen.fill("#C60045")
        self.world.tickPending()
        self.world.render(screen, self.camera)
        pygame.draw.circle(screen, "black", self.camera.vector(0, 0), 2)
        self.PAUSE_BUTTON.render(screen)
        self.SAVE_BUTTON.render(screen)
        self.HELP_BUTTON.render(screen)