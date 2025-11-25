from scene import *
import logging
import pygame
import utils.camera
import sweeper.world as sweeper_world

logger = logging.getLogger(__name__)

class GameScreen(Scene):
    camera = utils.camera.Camera() 
    world = sweeper_world.World(42)

    def input(self, events, kb_input):
        if kb_input[pygame.K_s]:
            self.camera.up()
        if kb_input[pygame.K_z]:
            self.camera.down()
        if kb_input[pygame.K_q]:
            self.camera.left()
        if kb_input[pygame.K_d]:
            self.camera.right()

    def render(self, screen):
        screen.fill("#4A4AD6")
        self.world.render(screen, self.camera)
        pygame.draw.circle(screen, "black", self.camera.vector(12, 24), 15)
        pygame.draw.circle(screen, "white", self.camera.vector(101, 54), 5)