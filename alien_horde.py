"""
Manages the alien horde mechanics for Alien Invasion.

This module handles the creation, positioning, and collision detection
of the alien sprite group.
"""

import pygame
from alien import Aliens
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

                # When aliens reach the bottom or kill the player
                self.descent_stage: bool = False

                # Create the horde
                self._create_horde()


        def _create_horde(self) -> None:
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


        def _check_collisions(self) -> None:
                """
                Handles collision detection for the edges of the screen, the player ship rect,
                and the laser rects.
                """

                screen_rect = self.game.screen.get_rect()

                # Only one pass through the aliens
                for alien in self.group.sprites():

                        # Check if any alien hits the bottom or collides with the player
                        if not self.descent_stage and (alien.rect.bottom >= screen_rect.bottom):
                                self.descent_stage = True
                                self.game.you_lose = True
                                break  # final descent takes priority

                        # Check if the horde hits screen edges (only if not advancing or descending)
                        if not self.advancing and not self.descent_stage and alien.check_edges():
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
                        False
                        )

                if ship_collisions and not self.descent_stage:
                        self.game.ship_group.empty()
                        pygame.mixer.Sound.play(pygame.mixer.Sound(self.settings.impact_noise))
                        self.descent_stage = True
                        self.game.you_lose = True

                # All aliens are dead, what now?
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
                """
                Update positions for each alien and handle edge collision logic.
                """

                # Only update if the game is not paused
                self._check_collisions()

                # If collision is an edge, advancing sets to true
                if self.advancing:

                        # How much to move this frame (this is an if-less if statement, it returns the smaller amount)
                        step = (
                                (self._advance_remaining * (self._advance_remaining < self.settings.horde_speed))
                                +
                                (self.settings.horde_speed * (self.settings.horde_speed <= self._advance_remaining))
                                )
                        if step > 0:
                                for alien in self.group.sprites():
                                        alien.rect.y += step
                                self._advance_remaining -= step

                        # If done advancing, reverse direction and clear state
                        if self._advance_remaining <= 0:
                                self.advancing = False
                                self._advance_remaining = 0
                                self.settings.horde_direction *= -1

                # If in final descent, move all aliens straight down
                if self.descent_stage:
                        for alien in self.group.sprites():
                                alien.rect.y += self.settings.horde_speed
                                if alien.rect.top > self.game.screen_rect.bottom:
                                        alien.kill()

                        if not self.group:
                                self.game.on_descent_complete()

                        return

                # Normal horizontal movement when not advancing/final
                if not self.advancing:
                        self.group.update()

        def reset(self) -> None:
                """
                Resets the horde for level advancing and life loss
                """

                self.group.empty()
                self.advancing = False
                self.descent_stage = False
                self._advance_remaining = 0
                self._create_horde()