"""
Horde building for the alien horde in the Alien Invasion game.

MORE HEREEEE
"""

import pygame
from alien import Aliens
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class AlienHorde:
        """EXPLAIN"""

        def __init__(self, game: 'AlienInvasion') -> None:
                self.game = game
                self.settings = game.settings
                self.horde = pygame.sprite.Group()
                self.direction = self.settings.horde_direction
                self.advance = self.settings.horde_advance

                self.create_horde()

        def create_horde(self):
                alien_size = self.settings.alien_size
                screen_size = self.settings.screen_size