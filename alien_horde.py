"""
Horde building for the alien horde in the Alien Invasion game.

TODO: Add laser colision detection and removal of individual sprites
"""

import pygame
from alien import Aliens
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class AlienHorde:
        """Houses the alien horde building mechanics."""

        def __init__(self, game: 'AlienInvasion') -> None:
                self.game = game
                self.settings = game.settings
                self.horde = pygame.sprite.Group()

                self._create_horde()

        def _create_horde(self):
                """
                Build a grid of aliens using rows and columns from settings.
                """
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
                                self.horde.add(alien)


        def _check_collisions(self):
                """
                Handles collision detection for the edge of the screen,the player ship rect,
                and the laser rects.
                """
                for alien in self.horde.sprites():
                        if alien.check_edges():
                                self._advance_and_reverse()
                                break
                pygame.sprite.groupcollide(
                        self.horde,
                        self.game.lasers,
                        True,
                        True
                        )

        def _advance_and_reverse(self):
                """
                Move the horde downward by one alien height
                and reverse horizontal direction.
                """
                for alien in self.horde.sprites():
                        alien.rect.y += self.settings.horde_advance
                self.settings.horde_direction *= -1

        def update(self):
                """
                Update positions for each alien and handle edge collision logic.
                """
                if not self.game.paused:
                        self._check_collisions()
                        self.horde.update()