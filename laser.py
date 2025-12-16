"""
Laser entities for the Alien Invasion game.

Provides sprite loading, positioning logic, and screen drawing behavior
for the ships lasers. Integrates with the main AlienInvasion game
instance to access window dimensions, settings, and display surfaces.
"""

from typing import TYPE_CHECKING
import pygame
from dataclasses import dataclass


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


@dataclass
class LaserData:
        """Holds laser position and size for clarity."""
        x: int
        y: int
        width: int
        height: int
        speed: int


class Laser(pygame.sprite.Sprite):
        """Houses the laser projectile surf, rect, and movement behavior."""

        # Initialize local variables
        def __init__(self, game: 'AlienInvasion', resources=None) -> None:

                # Initialize sprite class
                super().__init__()

                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings
                self.ship = game.ship

                # Main display surface and its bounding rectangle
                self.screen_image: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Position/size dataclass
                self.data = LaserData(
                        x=self.ship.rect.centerx,
                        y=self.ship.rect.top,
                        width=self.settings.laser_size[0],
                        height=self.settings.laser_size[1],
                        speed=self.settings.laser_speed
                )

                # Use preloaded image if available to reduce I/O
                if resources and "laser_image" in resources:
                        self.image: pygame.Surface = resources["laser_image"]
                else:
                        self.image: pygame.Surface = pygame.transform.scale(
                                pygame.image.load(self.settings.laser_graphic),
                                self.settings.laser_size
                        ).convert_alpha()

                # Rect for laser sprite
                self.rect: pygame.Rect = self.image.get_rect(center=(self.data.x, self.data.y))

                # Play laser noise if resource not preloaded
                if resources and "laser_sound" in resources:
                        self.laser_noise: pygame.mixer.Sound = resources["laser_sound"]
                        self.laser_noise.play()
                else:
                        self.laser_noise: pygame.mixer.Sound = pygame.mixer.Sound(self.settings.laser_noise)
                        self.laser_noise.play()

        def update(self) -> None:
                """Updates the lasers position."""

                # Move the laser
                self.rect.y -= self.data.speed

                # Delete the laser when it leaves the screen
                if self.rect.bottom < 0:
                        self.kill()
