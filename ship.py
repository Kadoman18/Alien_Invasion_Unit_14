"""
Ship entity for the Alien Invasion game.

Provides sprite loading, positioning logic, and screen drawing behavior
for the player's ship. Integrates with the main AlienInvasion game
instance to access window dimensions, settings, and display surfaces.
"""

import pygame
import paths
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Lab12_kbreinholt1_v2 import AlienInvasion


class Ship(pygame.sprite.Sprite):
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
                # Initialize sprite class (I think)
                super().__init__()

                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings

                # Surf and Rect for ship sprite
                self.screen: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                self.surf: pygame.Surface = pygame.transform.scale(pygame.image.load(paths.Graphics.ship1), self.settings.ship_size).convert_alpha()
                self.rect: pygame.Rect = self.surf.get_rect(midbottom = (
                        self.screen_rect.midbottom[0], self.screen_rect.midbottom[1] - (self.screen_rect.midbottom[1] // 100)
                        ))

                # Position ship centered horizontally and slightly above the bottom
                self.rect.midbottom = (
                        self.screen_rect.midbottom[0],
                        self.screen_rect.midbottom[1]
                        - (self.screen_rect.midbottom[1] // 75)
                )

                # Movement Bools for control using keyup/keydown based inputs
                self.moving_right: bool = False
                self.moving_left: bool = False
                self.firing: bool = False
                self.x = self.rect.x


        def update(self) -> None:
                """
                Updates the ships position.
                """

                # Padding to make the transition from side to side quicker
                buffer = 15

                # Firing Mechanics to slow the ship when firing
                # TODO: Not workinggg:)
                if self.firing:
                        self.speed = self.settings.ship_firing_speed
                        Laser.draw(Laser(self.game))
                else:
                        self.speed = self.settings.ship_speed

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
                """
                Draw the ship to the screen at its current position.
                """

                # Draw the ship to the screen
                self.screen.blit(self.surf, self.rect)


class Laser(pygame.sprite.Sprite):
        """
        Houses the laser projectile surf, rect, and movement behavior.
        """

        def __init__(self, game: 'AlienInvasion') -> None:
                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings
                self.ship = Ship(self.game)

                # Main display surface and its bounding rectangle
                self.screen: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Surf and Rect for laser sprite
                self.surf: pygame.Surface = pygame.transform.scale(pygame.image.load(paths.Graphics.laser), self.settings.laser_size).convert_alpha()
                self.rect: pygame.Rect = self.surf.get_rect(center = (self.ship.rect.midtop))

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
                self.screen.blit(self.surf, self.rect)

