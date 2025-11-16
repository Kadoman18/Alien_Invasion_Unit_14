"""
Laser entities for the Alien Invasion game.

Provides sprite loading, positioning logic, and screen drawing behavior
for the ships lasers. Integrates with the main AlienInvasion game
instance to access window dimensions, settings, and display surfaces.
"""

import pygame
import paths
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Lab12_kbreinholt1_v2 import AlienInvasion


class Laser(pygame.sprite.Sprite):
        """
        Houses the laser projectile surf, rect, and movement behavior.
        """

        def __init__(self, game: 'AlienInvasion') -> None:
                # Initialize sprite class (I think)
                super().__init__()
                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings
                self.ship = game.ship

                # Main display surface and its bounding rectangle
                self.screen: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Surf and Rect for laser sprite
                self.image: pygame.Surface = pygame.transform.scale(pygame.image.load(paths.Graphics.laser), self.settings.laser_size).convert_alpha()
                self.rect: pygame.Rect = self.image.get_rect(center = (self.ship.rect.midtop))

                # Sets the lasers travel speed
                self.speed: int = self.settings.laser_speed


        def update(self) -> None:
                """
                Updates the lasers position.
                """

                # Lasers movement
                self.rect.y -= self.speed

                # TODO: Kill the laser when it leaves the screen
                if self.rect.y < -5:
                        pass


        def draw(self) -> None:
                """
                Draw the ship to the screen at its current position.
                """

                # Draw the ship to the screen
                self.screen.blit(self.image, self.rect)

