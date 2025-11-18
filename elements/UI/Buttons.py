import pygame

class Button:
    def __init__(self, x, y, width, height, color, label: str, label_color = "white", font = "Helvetica", font_size = 20):
        self.color = color
        self.rect = pygame.Rect(x - width/2, y - height/2, width, height)
        self.font = pygame.font.SysFont(font, font_size)
        self.text = self.font.render(label, True, label_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def render(self, screen: pygame.Surface):
        self.screen = screen                                                            
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def hoverEvent(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        else:
            return False

    def alterColor(self, color):
        pygame.draw.rect(self.screen, color, self.rect)

    def reset(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class BasicButton(Button):
    def __init__(self, x, y, label = "Default Label"):
        super().__init__(x, y, 100, 50, "#464646", label)

    def alterColor(self, color = "#797979"):
        return super().alterColor(color)