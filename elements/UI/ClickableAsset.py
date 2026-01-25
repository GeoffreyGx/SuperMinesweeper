import pygame
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ClickableAsset:
    def __init__(self, asset: str, x: float, y: float, width: Optional[float] = None, height: Optional[float] = None, asset_hov: Optional[str] = None) -> None:
        self.asset = pygame.image.load("assets/ui/" + asset + ".png")
        self.width = float(width) if width is not None else float(self.asset.get_width())
        self.height = float(height) if height is not None else float(self.asset.get_height())
        if (self.asset.get_width(), self.asset.get_height()) != (int(self.width), int(self.height)):
            self.asset = pygame.transform.scale(self.asset, (int(self.width), int(self.height)))
        self.rect = pygame.Rect(0, 0, int(self.width), int(self.height))
        self.rect.center = (int(x), int(y))
        try:
            self.asset_hov = pygame.image.load("assets/ui/" + asset_hov + ".png") if asset_hov is not None else pygame.image.load("assets/ui/" + asset + ".hov.png")
        except:
            logger.warning(asset + " is missing a hovering asset")
        else:
            if (self.asset_hov.get_width(), self.asset_hov.get_height()) != (int(self.width), int(self.height)):
                self.asset_hov = pygame.transform.scale(self.asset_hov, (int(self.width), int(self.height)))
        self.hovered = False


    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle a single pygame event. Returns True if the button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def render(self, screen: pygame.Surface):
        if self.hovered:
            try:
                screen.blit(self.asset_hov, self.rect)
            except:
                screen.blit(self.asset, self.rect)
        else:
            screen.blit(self.asset, self.rect)