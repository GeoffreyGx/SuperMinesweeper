import pygame
from typing import Callable, Optional, Tuple
class Button:
    """A simple, reusable UI Button for pygame scene-based apps.

    Usage:
      btn = Button(x, y, width, height, label="Click", callback=on_click)
      In your scene.input(events):
          for e in events:
              btn.handle_event(e)
      In your scene.render(screen):
          btn.draw(screen)
    """

    def __init__(self, x: float, y: float, width: int, height: int, label: str = "", bg: str = "#464646", fg: str = "white", hover_bg: str = "#535353", pressed_bg: str = "black", font_name: Optional[str] = None, font_size: int = 20, action: Optional[str] = None):
        self.rect = pygame.Rect(0, 0, int(width), int(height))
        self.rect.center = (int(x), int(y))

        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.pressed_bg = pressed_bg

        self.font = pygame.font.SysFont(font_name or pygame.font.get_default_font(), font_size)
        self.label = label
        self._render_label()

        self.hovered = False
        self.pressed = False

        self.action = action

    def _render_label(self):
        self.text_surf = self.font.render(self.label, True, self.fg)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def set_center(self, x: float, y: float):
        self.rect.center = (int(x), int(y))
        self.text_rect.center = self.rect.center

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a single pygame event. Returns True if the button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def getAction(self):
        if self.action != None:
            return self.action
        return False

    def draw(self, screen: pygame.Surface):
        # pick color based on state
        if self.pressed:
            color = self.pressed_bg
        elif self.hovered:
            color = self.hover_bg
        else:
            color = self.bg

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        screen.blit(self.text_surf, self.text_rect)


class BasicButton(Button):
    """Small centered button with sensible defaults."""

    def __init__(self, x: float, y: float, label: str = "Button", action = None):
        super().__init__(x, y, 140, 48, label, action=action, bg="#464646", fg="#FFFFFF", font_size=18)