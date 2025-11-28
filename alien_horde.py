"""
Horde building for the alien horde in the Alien Invasion game.

MORE HEREEEE
"""

import pygame
from alien import Aliens
from typing import TYPE_CHECKING

# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class AlienHorde:
        """EXPLAIN"""

        def __init__(self, game: 'AlienInvasion') -> None:
                self.game = game
                self.settings = game.settings
                self.horde = pygame.sprite.Group()

                self._create_horde()

        def _create_horde(self):
                """
                Build a grid of aliens using rows and columns from settings.
                """

                alien_width = self.settings.alien_size[0]
                alien_height = self.settings.alien_size[1]
                for row in range(self.settings.horde_size[0]):
                        for col in range(self.settings.horde_size[1]):
                                alien = Aliens(self.game, alien_width, alien_height)

                                padding = self.settings.horde_padding

                                alien.rect.x = alien_width + padding + (col * (alien_width + padding))
                                alien.rect.y = alien_height + padding + (row * (alien_height + padding))

                                self.horde.add(alien)

        def update(self):
                """
                Update positions for each alien and handle edge collision logic.
                """
                self._check_edges()
                self.horde.update()

        def _check_edges(self):
                """
                If any alien hits an edge, move fleet downward and reverse direction.
                """
                for alien in self.horde.sprites():
                        if alien.check_edges():
                                self._advance_and_reverse()
                                break

        def _advance_and_reverse(self):
                """
                Move the horde downward by one alien height
                and reverse horizontal direction.
                """
                for alien in self.horde.sprites():
                        alien.rect.y += self.settings.horde_advance
                self.settings.horde_direction *= -1