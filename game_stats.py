"""
"""

import pygame
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Alien_Invasion import AlienInvasion


class GameStats:
        """
        """
        def __init__(self, game: 'AlienInvasion'):
                """
                """
                self.game = game
                self.settings = game.settings
                self.max_score: int = 0
                self.init_saved_scores()
                self.reset_stats(game)
                self.wave: int = 1


        def init_saved_scores(self) -> None:
                """
                """
                self.path = self.settings.score_file
                if self.path.exists() and self.path.stat().st_size > 0:
                    contents = self.path.read_text()
                    scores = json.loads(contents)
                    self.hi_score = scores.get('hi_score', 0)
                else:
                    self.hi_score = 0
                    self.save_scores()


        def save_scores(self) -> None:
                """
                """
                scores = {'hi_score': self.hi_score}
                contents = json.dumps(scores, indent=4)
                try:
                    self.path.write_text(contents)
                except FileNotFoundError as e:
                    print("File not found!:", e)


        def reset_stats(self, game: 'AlienInvasion') -> None:
                """
                """
                self.lives_left = game.settings.starting_lives
                self.score = 0
                self.wave = 1


        def update(self, collisions: dict[pygame.sprite.Sprite, list[pygame.sprite.Sprite]]) -> None:
                """
                """
                self._update_score(collisions)
                self._update_hi_score()


        def _update_hi_score(self) -> None:
                """
                """
                if self.score > self.hi_score:
                    self.hi_score = self.score
                    self.save_scores()


        def _update_score(self, collisions: dict) -> None:
                """
                """
                for alien in collisions.values():
                    self.score += self.settings.alien_value


        def update_wave(self) -> None:
                """
                """
                self.wave += 1