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

                # Initialize horde group
                self.group = pygame.sprite.Group()

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

                # Advance when the horde hits the edges of the screen
                for alien in self.group.sprites():
                        if alien.check_edges():
                                self._advance_and_reverse()
                                break

                # Delete self and laser when alien in horde is shot
                laser_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.lasers,
                        True,
                        True
                        )

                # Play destruct sound effect (it seemed long so I shortened it)
                if laser_collisions:
                        pygame.mixer.Sound(self.settings.impact_noise).play(0, 300, 0)
                ship_collisions = pygame.sprite.groupcollide(
                        self.group,
                        self.game.ship_group,
                        False,
                        True
                )

                # End the game if the player encounters the aliens (if not debugging)
                if ship_collisions:
                        if self.settings.DEBUGGING:
                                self.game.running = True
                        else:
                                pygame.time.delay(1200)
                                self.game.running = False

                # End the game if all of the aliens die
                if len(self.group.sprites()) <= 0:
                        pygame.time.delay(1200)
                        self.game.running = False


        def _advance_and_reverse(self):
                """
                Move the horde downward by one alien height and reverse horizontal
                direction.
                """

                # Advance the alien horde
                for alien in self.group.sprites():
                        alien.rect.y += self.settings.horde_advance

                # Reverse the travel direction of the horde
                self.settings.horde_direction *= -1


        def update(self):
                """
                Update positions for each alien and handle edge collision logic.
                """

                # Only update if the game is not paused
                if not self.game.paused:
                        self._check_collisions()
                        self.group.update()