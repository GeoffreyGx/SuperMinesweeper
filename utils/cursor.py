import pygame

class Cursor:
    def __init__(self, path = './assets/cursors/arrow.png'):
        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load(path)
        self.cursor_img_rect = self.cursor_img.get_rect()

    def update(self, display):
        self.cursor_img_rect.center = pygame.mouse.get_pos() 
        display.blit(self.cursor_img, self.cursor_img_rect)

    def change(self, type):
        self.__init__('./assets/cursors/' + type + '.png')