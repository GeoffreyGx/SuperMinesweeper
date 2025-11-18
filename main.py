VERSION = "ALPHA 0.0.1"

import logging
import pygame
import utils.camera as camera
import utils.cursor as cursor
import scenes.MainMenu as MainMenu

logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(module)s] %(levelname)s - %(message)s', datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
pygame.init()
pygame.font.init()
pygame.display.set_caption("SuperMinesweeper " + VERSION)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


def main():
    logger.info('Welcome to SuperMinesweeper %s', VERSION)
    running = True

    active_scene = MainMenu.MainMenu()
    
    while running:
        # Pull events once and reuse them so scenes receive the same event list
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        active_scene.input(events, pygame.key.get_pressed())
        active_scene.update()
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()