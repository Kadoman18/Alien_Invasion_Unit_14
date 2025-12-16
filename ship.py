"""
Ship entity for the Alien Invasion game.
"""

from laser import Laser
from typing import TYPE_CHECKING
import pygame
from dataclasses import dataclass


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


@dataclass
class ShipState:
        """Dataclass to hold movement and firing state for the ship"""
        moving_right: bool = False
        moving_left: bool = False
        firing: bool = False
        firing_rapid: bool = False
        last_shot_time: int = 0


class Ship(pygame.sprite.Sprite):
        """Represents the player's ship in the game world."""

        # Initialize local variables
        def __init__(self, game: 'AlienInvasion', resources=None) -> None:

                # Initialize sprite class
                super().__init__()

                # Basic references to AlienInvasion class and Settings class
                self.game = game
                self.settings = game.settings
                self.resources = resources

                # Main display surface and its bounding rectangle
                self.screen_image: pygame.Surface = game.screen
                self.screen_rect: pygame.Rect = game.screen_rect

                # Load ship image from preloaded resources if provided
                if self.resources:
                        self.image: pygame.Surface = pygame.transform.scale(
                                self.resources.ship_image,
                                self.settings.ship_size
                        ).convert_alpha()
                else:
                        self.image: pygame.Surface = pygame.transform.scale(
                                pygame.image.load(self.settings.ship_image),
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

                # Movement & firing state dataclass
                self.state: ShipState = ShipState()

        def _fire_laser(self) -> None:
                """Handles the logic for continuous laser firing and rate"""

                # Don't fire while the game is paused or the player has lost
                if self.game.paused or self.game.you_lose:
                        return

                # Relative time for pause
                now = pygame.time.get_ticks()
                relative_now = now - self.game.pause_duration

                # Base fire
                if self.state.firing and (relative_now - self.state.last_shot_time >= self.settings.ship_base_fire_rate):
                        self.game.lasers.add(Laser(self.game))
                        self.state.last_shot_time = relative_now

                # Rapid fire
                elif self.state.firing and self.state.firing_rapid and (
                    relative_now - self.state.last_shot_time >= self.settings.ship_rapid_fire_rate
                ):
                        self.game.lasers.add(Laser(self.game))
                        self.state.last_shot_time = relative_now

        def update(self) -> None:
                """Update ship position and firing based on key press flags."""

                # Fire lasers if conditions are met
                self._fire_laser()

                # Firing slows ship
                speed: int = self.settings.ship_speed
                if self.state.firing and self.state.firing_rapid:
                        speed = self.settings.ship_rapid_firing_speed
                elif self.state.firing:
                        speed = self.settings.ship_base_firing_speed

                # Rightward movement and wrapping
                if self.state.moving_right:
                        self.rect.x += speed
                        if self.rect.left > self.settings.screen_size[0] - self.settings.ship_wrap_buffer:
                                self.rect.right = self.settings.ship_wrap_buffer

                # Leftward movement and wrapping
                if self.state.moving_left:
                        self.rect.x -= speed
                        if self.rect.right < self.settings.ship_wrap_buffer:
                                self.rect.left = self.settings.screen_size[0] - self.settings.ship_wrap_buffer
