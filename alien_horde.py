"""
Manages the alien horde mechanics for Alien Invasion.

This module handles the creation, positioning, and collision detection
of the alien sprite group.
"""

import pygame
from alien import Aliens
from typing import TYPE_CHECKING
from dataclasses import dataclass


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


@dataclass
class HordeState:
        spawning: bool = True
        spawn_remaining: int = 0
        advancing: bool = False
        advance_remaining: int = 0
        descent_stage: bool = False



class AlienHorde:
        """Houses the alien horde building mechanics."""

        # Initialize local variables
        def __init__(self, game: 'AlienInvasion', resources=None) -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings
                self.stats = game.stats
                self.resources = resources

                # Initialize horde group
                self.group = pygame.sprite.Group()

                # Horde state
                self.state = HordeState()

                # Create the horde
                self._create_horde()

        def _create_horde(self) -> None:
                padding: int = self.settings.horde_padding
                alien_size: tuple[int, int] = self.settings.alien_size

                # How far the horde must descend before becoming active
                total_height = (
                        self.settings.horde_size[0] * alien_size[1] +
                        (self.settings.horde_size[0] - 1) * padding
                )

                self.state.spawning = True
                self.state.spawn_remaining = total_height + alien_size[1] + padding


                for row in range(self.settings.horde_size[0]):
                        for col in range(self.settings.horde_size[1]):
                                alien = (
                                        Aliens(self.game, alien_size[0], alien_size[1], self.resources)
                                        if self.resources
                                        else Aliens(self.game, alien_size[0], alien_size[1])
                                )

                                alien.rect.center = (
                                        alien_size[0] + padding + (col * (alien_size[0] + padding)),
                                        # start above screen
                                        -total_height + (row * (alien_size[1] + padding))
                                )

                                self.group.add(alien)

        def _check_collisions(self) -> None:
                """
                Handles collision detection for the edges of the screen, the player ship rect,
                and the laser rects.
                """
                screen_rect = self.game.screen.get_rect()

                # Only one pass through the aliens
                for alien in self.group.sprites():

                        # Check if any alien hits the bottom or collides with the player
                        if not self.state.descent_stage and (alien.rect.bottom >= screen_rect.bottom):
                                self.state.descent_stage = True
                                self.game.you_lose = True
                                break  # final descent takes priority

                        # Check if the horde hits screen edges (only if not advancing or descending)
                        if not self.state.advancing and not self.state.descent_stage and alien.check_edges():
                                self.state.advancing = True
                                self.state.advance_remaining = self.settings.horde_advance
                                break

                # Delete self and laser when alien in horde is shot
                laser_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.lasers,
                        True,
                        True
                        )

                # Play destruct sound effect (shortened for performance)
                for collision in laser_collisions:
                        pygame.mixer.Sound(self.settings.impact_noise).play(0, 325, 0)

                        # Add value of alien to score
                        self.stats.update(laser_collisions)
                        print(f"Score: {self.stats.score}")

                ship_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.ship_group,
                        False,
                        False
                        )

                if ship_collisions and not self.state.descent_stage:
                        self.game.ship_group.empty()
                        pygame.mixer.Sound.play(pygame.mixer.Sound(self.settings.impact_noise))
                        self.state.descent_stage = True
                        self.game.you_lose = True

                # All aliens are dead, advance wave
                if not self.group and not self.game.you_lose:
                        self.stats.update_wave()
                        self.reset()

        def _advance_and_reverse(self) -> None:
                """
                Move the horde downward by one alien height and reverse horizontal
                direction.
                """
                # (Kept for compatibility) instant advance + reverse. The
                # preferred path is the timed advance performed in `update`.
                for alien in self.group.sprites():
                        alien.rect.y += self.settings.horde_advance
                self.settings.horde_direction *= -1

        def update(self) -> None:
                # Spawn phase: move horde down, disable gameplay
                if self.state.spawning:
                        step = min(self.state.spawn_remaining, self.settings.horde_speed)
                        if step > 0:
                                for alien in self.group.sprites():
                                        alien.rect.y += step
                                self.state.spawn_remaining -= step

                        if self.state.spawn_remaining <= 0:
                                self.state.spawning = False
                                self.state.spawn_remaining = 0
                                self.game.on_horde_spawn_complete()
                        return

                # If in final descent, move all aliens straight down
                if self.state.descent_stage:
                        for alien in self.group.sprites():
                                alien.rect.y += self.settings.horde_speed
                                if alien.rect.top > self.game.screen_rect.bottom:
                                        alien.kill()

                        if not self.group:
                                self.game.on_descent_complete()
                        return

                # Advance phase: move horde down over time, then reverse
                if self.state.advancing:
                        step = min(self.state.advance_remaining, self.settings.horde_speed)

                        for alien in self.group.sprites():
                                alien.rect.y += step

                        self.state.advance_remaining -= step

                        if self.state.advance_remaining <= 0:
                                self.state.advancing = False
                                self.state.advance_remaining = 0
                                self.settings.horde_direction *= -1

                        return

                # Normal horizontal movement
                self.group.update()
                self._check_collisions()

        def reset(self) -> None:
                """
                Resets the horde for level advancing and life loss
                """
                self.group.empty()
                self.state = HordeState()
                self._create_horde()
