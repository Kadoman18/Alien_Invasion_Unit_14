"""
"""

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
                self.max_score = 0
                self.init_saved_scores()
                self.reset_stats(game)


        def init_saved_scores(self):
                """
                """
                self.path = self.settings.scores_file
                if self.path.exists() and self.path.stat().st_size > 0:
                    contents = self.path.read_text()
                    scores = json.loads(contents)
                    self.hi_score = scores.get('hi_score', 0)
                else:
                    self.hi_score = 0
                    self.save_scores()


        def save_scores(self):
                """
                """
                scores = {'hi_score': self.hi_score}
                contents = json.dumps(scores, indent=4)
                try:
                    self.path.write_text(contents)
                except FileNotFoundError as e:
                    print("File not found!:", e)


        def reset_stats(self, game: 'AlienInvasion'):
                """
                """
                self.hero_ships_left = game.settings.starting_lives
                self.score = 0
                self.wave = 1


        def update(self, collisions: dict):
                """
                """
                self._update_score(collisions)
                self._update_max_score()
                self._update_hi_score()


        def _update_max_score(self):
                """
                """
                if self.score > self.max_score:
                    self.max_score = self.score
                print("MAX:", self.max_score)


        def _update_hi_score(self):
                """
                """
                if self.score > self.hi_score:
                    self.hi_score = self.score
                    self.save_scores()
                print("HI:", self.hi_score)


        def _update_score(self, collisions: dict):
                """
                """
                for alien in collisions.values():
                    self.score += self.settings.alien_value
                print("SCORE:", self.score)


        def update_wave(self):
                """
                """
                self.wave += 1
                print("Wave:", self.wave)