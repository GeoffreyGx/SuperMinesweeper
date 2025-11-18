from scene import *
import logging
import pygame
import utils.camera

logger = logging.getLogger(__name__)

class GameScreen(Scene):
    camera = utils.camera.Camera() 

    def input(self, events, kb_input):
        if kb_input[pygame.K_z]:
            self.camera.up()
        if kb_input[pygame.K_s]:
            self.camera.down()
        if kb_input[pygame.K_q]:
            self.camera.left()
        if kb_input[pygame.K_d]:
            self.camera.right()

    def render(self, screen):
        screen.fill("#4A4AD6")
        pygame.draw.circle(screen, "black", self.camera.vector(12, 24), 15)
        pygame.draw.circle(screen, "white", self.camera.vector(101, 54), 5)