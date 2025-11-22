"""
Alien entities for the Alien Invasion game.

Provides sprite loading, positioning logic, and screen drawing behavior
for the alien ship. Integrates with the main AlienInvasion game
instance to access window dimensions, settings, and display surfaces.
"""

import pygame
import paths
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class Aliens(pygame.sprite.Sprite):
        """Houses the alien surf, rect, and movement behavior."""

        def __init__(self, game: 'AlienInvasion', x: int, y: int) -> None:

                # Initialize sprite class
                super().__init__()

                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings
                self.ship = game.ship

                # Main display surface and its bounding rectangle
                self.screen_image: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Surf and rect for alien sprite
                self.image: pygame.Surface = pygame.transform.scale(pygame.image.load(paths.Graphics.alien), self.settings.alien_size).convert_alpha()
                self.rect: pygame.Rect = self.image.get_rect(center = (x, y))

                # Set the aliens travel speed
                self.speed: int = self.settings.alien_speed

                # Movement bools
                self.moving_right: bool  = False
                self.moving_left: bool  = False


        def update(self) -> None:
                """Updates the aliens position."""

                # Alien movement
                if self.moving_right:
                        self.rect.x += self.speed
                elif self.moving_left:
                        self.rect.x -= self.speed

