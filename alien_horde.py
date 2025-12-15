"""
Manages the alien horde mechanics for Alien Invasion.

This module handles the creation, positioning, and collision detection
of the alien sprite group.
"""

import pygame
from alien import Aliens
from game_stats import GameStats
from typing import TYPE_CHECKING


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class AlienHorde:
        """Houses the alien horde building mechanics."""

        # Initialize local variables
        def __init__(self, game: 'AlienInvasion') -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings
                self.stats = game.stats

                # Initialize horde group
                self.group = pygame.sprite.Group()

                # State for when horde is advancing downward (edge-triggered)
                self.advancing: bool = False

                # Remaining advance distance for edge-triggered advance
                self._advance_remaining: int = 0

                # When aliens reach the bottom, enter final descent mode:
                # move straight down (no horizontal movement) until off-screen,
                # then wait and end the game.
                self.final_descend: bool = False

                # Create the horde
                self._create_horde()


        def _create_horde(self):
                """Build a grid of aliens using rows and columns from settings."""

                # Spacing between aliens
                padding: int = self.settings.horde_padding

                # Extract alien measurments from settings
                alien_size: tuple[int, int] = self.settings.alien_size

                # Build the horde to set specifications
                for row in range(self.settings.horde_size[0]):
                        for col in range(self.settings.horde_size[1]):
                                alien = Aliens(self.game, alien_size[0], alien_size[1])

                                # Define the current aliens rect
                                alien.rect.center = (
                                        alien_size[0] + padding + (col * (alien_size[1] + padding)),
                                        alien_size[0] + padding + (row * (alien_size[1] + padding))
                                        )

                                # Add the current alien to horde sprite group
                                self.group.add(alien)


        def _check_collisions(self):
                """
                Handles collision detection for the edges of the screen, the player ship rect,
                and the laser rects.
                """

                # If any alien reaches the bottom of the screen, enter final
                # descent mode: freeze horizontal movement, freeze the ship,
                # and move straight down until all aliens are off-screen.
                screen_rect = self.game.screen.get_rect()
                if not self.final_descend:
                        for alien in self.group.sprites():
                                if alien.rect.bottom >= screen_rect.bottom:
                                        self.final_descend = True
                                        # freeze player controls
                                        self.game.you_lose = True
                                        break

                # Start advancing when the horde hits the left/right edges of the screen.
                # We don't immediately reverse here; instead we set an advancing
                # state so the horde moves down over time at the configured
                # horde/alien speed, then reverse when the advance completes.
                if not self.advancing and not self.final_descend:
                        for alien in self.group.sprites():
                                if alien.check_edges():
                                        # Begin an advance equal to one alien height
                                        self.advancing = True
                                        self._advance_remaining = self.settings.horde_advance
                                        break

                # Delete self and laser when alien in horde is shot
                laser_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.lasers,
                        True,
                        True
                        )

                # Play destruct sound effect (it seemed long so I shortened it)
                for collision in laser_collisions:
                        pygame.mixer.Sound(self.settings.impact_noise).play(0, 325, 0)

                        # Add value of alien to score
                        self.stats.update(laser_collisions)
                        print(f"Score: {self.stats.score}")

                ship_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.ship_group,
                        False,
                        True
                )

                # End the game if the player is killed by the aliens
                if ship_collisions:
                        if self.settings.DEBUGGING:
                                self.game.you_lose = False
                                self.final_descend = True
                                pygame.mixer.Sound(self.settings.impact_noise).play()
                        else:
                                self.game.you_lose = True
                                self.final_descend = True
                                pygame.mixer.Sound(self.settings.impact_noise).play()

                # All aliens are dead, what now?
                if len(self.group.sprites()) <= 0:

                        # Aliens defeated, new wave
                        if not self.game.you_lose:
                                pygame.time.delay(1200)
                                self._create_horde()
                                self.stats.update_wave()

                        # Aliens win, game over
                        else:
                                pygame.time.delay(1200)
                                self.game.running = False



        def _advance_and_reverse(self):
                """
                Move the horde downward by one alien height and reverse horizontal
                direction.
                """
                # (Kept for compatibility) instant advance + reverse. The
                # preferred path is the timed advance performed in `update`.
                for alien in self.group.sprites():
                        alien.rect.y += self.settings.horde_advance
                self.settings.horde_direction *= -1


        def update(self):
                """
                Update positions for each alien and handle edge collision logic.
                """

                # Only update if the game is not paused
                if not self.game.paused:

                        # First, detect collisions
                        self._check_collisions()

                        # If collision is an edge, advancing sets to true
                        if self.advancing:

                                # How much to move this frame
                                step = min(self._advance_remaining, abs(self.settings.horde_speed))
                                if step > 0:
                                        for alien in self.group.sprites():
                                                alien.rect.y += step
                                        self._advance_remaining -= step

                                # If done advancing, reverse direction and clear state
                                if self._advance_remaining <= 0:
                                        self.advancing = False
                                        self._advance_remaining = 0
                                        self.settings.horde_direction *= -1

                        # If we're in final descent mode, move all aliens straight
                        # down at the configured speed until they exit the screen.
                        if self.final_descend:
                                step = abs(self.settings.horde_speed) or 1
                                for alien in self.group.sprites():
                                        alien.rect.y += step

                                # If all aliens have moved entirely off the bottom,
                                # wait 1 second then end the game.
                                if all(a.rect.top > self.game.screen_rect.bottom for a in self.group.sprites()):
                                        pygame.time.delay(1000)
                                        self.game.running = False
                                return

                        # Normal horizontal movement when not advancing/final
                        if not self.advancing:
                                self.group.update()