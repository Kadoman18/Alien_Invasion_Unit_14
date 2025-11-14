"""
Ship entity for the Alien Invasion game.

Provides sprite loading, positioning logic, and screen drawing behavior
for the player's ship. Integrates with the main AlienInvasion game
instance to access window dimensions, settings, and display surfaces.
"""

import pygame
import paths
import hud
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Lab12_kbreinholt1_v2 import AlienInvasion


class Ship:
        """
        Represents the player's ship in the game world.

        Handles loading the ship sprite, computing its initial position,
        and rendering it onto the main game surface.
        """

        def __init__(self, game: 'AlienInvasion') -> None:
                """
                Initialize the ship and its rendering properties.

                Parameters
                ----------
                game : AlienInvasion
                        Reference to the main game instance, supplying
                        settings, screen surfaces, and layout dimensions.
                """
                self.game = game
                self.settings = game.settings

                # Main display surface and its bounding rectangle
                self.screen: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Create ship sprite using HUD's generic sprite loader
                self.ship_sprite = hud.make_custom_sprite(
                        paths.Graphics.ship1,
                        self.settings.ship_size
                )

                # Extract sprite components
                self.surf: pygame.Surface = self.ship_sprite.surf
                self.rect: pygame.Rect = self.ship_sprite.rect

                # Position ship centered horizontally and slightly above the bottom
                self.rect.midbottom = (
                        self.screen_rect.midbottom[0],
                        self.screen_rect.midbottom[1]
                        - (self.screen_rect.midbottom[1] // 75)
                )

        def draw(self) -> None:
                """
                Draw the ship to the screen at its current position.
                """
                self.screen.blit(self.surf, self.rect)
