VERSION = "ALPHA 0.0.1"

import pygame
import camera

pygame.init()
pygame.display.set_caption("SuperMinesweeper " + VERSION)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_camera = camera.Camera()

def main():
    print('Welcome to SuperMinesweeper', VERSION)
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("#DCDCDC")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            game_camera.up()
        if keys[pygame.K_s]:
            game_camera.down()
        if keys[pygame.K_q]:
            game_camera.left()
        if keys[pygame.K_d]:
            game_camera.right()
        pygame.draw.circle(screen, '#000000', pygame.Vector2(720+game_camera.RELATIVE_X, 100+game_camera.RELATIVE_Y), 20)
        pygame.draw.circle(screen, '#000000', pygame.Vector2(720+game_camera.RELATIVE_X, 200+game_camera.RELATIVE_Y), 20)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()