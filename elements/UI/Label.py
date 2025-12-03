import pygame

class Label:
    def __init__(self, x: int, y: int, text: str) -> None:
        self.x = x
        self.y = y
        self.text = text
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
        
        self.text_surface = self.font.render('Some Text', False, (0, 0, 0))


    def draw(self, display: pygame.Surface) -> None:
        display.blit(self.text_surface)