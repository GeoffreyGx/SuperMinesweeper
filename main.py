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
# game_cursor = cursor.Cursor() 


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
        # screen.fill("#DCDCDC")

        # mouse_rel = pygame.mouse.get_rel()
        # mouse = pygame.mouse.get_pressed()
        # if mouse[0]:
        #     game_cursor.change('hand_drag')
        #     game_camera.down(mouse_rel[1])
        #     game_camera.left(mouse_rel[0])
        
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_z]:
        #     game_camera.up()
        # if keys[pygame.K_s]:
        #     game_camera.down()
        # if keys[pygame.K_q]:
        #     game_camera.left()
        # if keys[pygame.K_d]:
        #     game_camera.right()

        # pygame.draw.circle(screen, '#000000', game_camera.vector(10, 20), 20)
        # pygame.draw.circle(screen, "#9713C7", game_camera.vector(103, 120), 15)
        
        # game_cursor.update(screen)
        # game_cursor.change('arrow')
        
        # Pass the collected events to the active scene so it can handle KEYDOWN etc.
        
        active_scene.input(events, pygame.key.get_pressed())
        active_scene.update()
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()