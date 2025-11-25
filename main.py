import logging
import pygame
import dotenv
import os
import utils.camera as camera
import utils.cursor as cursor
import scenes.MainMenu as MainMenu

dotenv.load_dotenv(".env")

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(module)s] %(levelname)s - %(message)s', datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
pygame.init()
pygame.font.init()
pygame.display.set_caption("SuperMinesweeper " + str(os.getenv("VERSION")))
screen = pygame.display.set_mode((int(str(os.getenv("SCREEN_WIDTH"))), int(str(os.getenv("SCREEN_HEIGHT")))))
clock = pygame.time.Clock()

def main():
    logger.info('Welcome to SuperMinesweeper %s', str(os.getenv("VERSION")))
    running = True

    active_scene = MainMenu.MainMenu()
    
    while running:
        # Pull events once and reuse them so scenes receive the same event list
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        active_scene.update()
        active_scene.input(events, pygame.key.get_pressed())
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()