"""
Ship entity for the Alien Invasion game.
"""

import pygame
import paths
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class Ship(pygame.sprite.Sprite):
        """Represents the player's ship in the game world."""

        def __init__(self, game: 'AlienInvasion') -> None:

                # Initialize sprite class
                super().__init__()

                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings

                # Main display surface and its bounding rectangle
                self.screen_image: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Load ship image and create surface
                self.image: pygame.Surface = pygame.image.load(paths.Graphics.ship).convert_alpha()
                self.image: pygame.Surface = pygame.transform.scale(
                        pygame.image.load(paths.Graphics.ship),
                        self.settings.ship_size
                ).convert_alpha()

                # Rect for sprite
                self.rect: pygame.Rect = self.image.get_rect()

                # Position ship centered horizontally and slightly above the bottom
                self.rect.midbottom = (
                        self.screen_rect.midbottom[0],
                        self.screen_rect.midbottom[1]
                        - (self.screen_rect.midbottom[1] // 75)
                )

                # Movement flags
                self.moving_right: bool = False
                self.moving_left: bool = False

                # Firing flags
                self.firing: bool = False
                self.firing_rapid: bool = False


        def update(self) -> None:
                """Update ship position based on movement flags."""

                # Padding to make the transition from side to side quicker
                buffer: int = 15

                # Firing slows ship
                self.speed: int  = self.settings.ship_speed
                if self.firing and self.firing_rapid:
                        self.speed: int  = self.settings.ship_rapid_firing_speed
                elif self.firing:
                        self.speed: int = self.settings.ship_base_firing_speed

                # Rightward movement and wrapping
                if self.moving_right:
                        self.rect.x += self.speed
                        if self.rect.left > self.settings.screen_size[0] - buffer:
                                self.rect.right = buffer

                # Leftward movement and wrapping
                if self.moving_left:
                        self.rect.x -= self.speed
                        if self.rect.right < buffer:
                                self.rect.left = self.settings.screen_size[0] - buffer


        def draw(self) -> None:
                """Draw the ship."""

                # Draw the ship
                self.screen_image.blit(self.image, self.rect)
