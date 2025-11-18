import logging
import pygame

class Scene:
    def __init__(self):
        self.next = self
        self._warned_methods = set()
        self.logger = logging.getLogger(__class__.__name__)

    def input(self, events, kb_input):
        if 'input' not in self._warned_methods:
            self.logger.warning("Input method hasn't been overridden for %s", self.__class__.__name__)
            self._warned_methods.add('input')
    
    def update(self):
        if 'update' not in self._warned_methods:
            self.logger.warning("Update method hasn't been overridden for %s", self.__class__.__name__)
            self._warned_methods.add('update')
    
    def render(self, screen: pygame.Surface):
        if 'render' not in self._warned_methods:
            self.logger.warning("Render method hasn't been overridden for %s", self.__class__.__name__)
            self._warned_methods.add('render')

    def switch(self, next_scene):
        self.next = next_scene