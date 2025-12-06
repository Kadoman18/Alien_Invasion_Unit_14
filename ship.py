"""
Ship entity for the Alien Invasion game.
"""

import pygame
from arsenal import Laser
import settings
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
                self.image: pygame.Surface = pygame.image.load(settings.Graphics.ship).convert_alpha()
                self.image: pygame.Surface = pygame.transform.scale(
                        pygame.image.load(settings.Graphics.ship),
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
                self.last_shot_time = 0
                self.firing: bool = False
                self.firing_rapid: bool = False


        def _fire_laser(self) -> None:
                """Handles the logic for continuous laser firing and rate"""
                if self.game.paused:
                        return

                now = pygame.time.get_ticks()
                relative_now = now - self.game.pause_duration

                # Base fire
                if self.game.ship.firing and (relative_now - self.last_shot_time >= self.settings.ship_base_fire_rate):
                        self.game.lasers.add(Laser(self.game))
                        self.last_shot_time = relative_now

                # Rapid fire
                elif self.game.ship.firing and self.game.ship.firing_rapid and (
                    relative_now - self.last_shot_time >= self.settings.ship_rapid_fire_rate
                ):
                        self.game.lasers.add(Laser(self.game))
                        self.last_shot_time = relative_now


        def update(self) -> None:
                """Update ship position and firing based on key press flags."""

                # Fire lasers if conditions are met
                self._fire_laser()

                # Padding to make the transition from side to side quicker
                buffer: int = 15
                if not self.game.paused:
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
