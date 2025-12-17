"""
Manages game statistics for Alien Invasion.
"""
import pygame
import json
from typing import TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from Alien_Invasion import AlienInvasion
    from pathlib import Path


@dataclass
class GameStats:
        """
        Stores statistics for the current game session, including score, wave, and lives.
        """

        game: 'AlienInvasion'
        settings: 'AlienInvasion.settings' = field(init=False) # <-works, but vsc thinks its wrong
        lives_left: int = field(init=False)
        score: int = field(init=False)
        wave: int = field(init=False, default=1)
        hi_score: int = field(init=False, default=0)
        path: 'Path' = field(init=False)

        def __post_init__(self):
                self.settings = self.game.settings
                self.path = self.settings.score_file
                self.init_saved_scores()
                self.reset_stats()
                self.wave = 1


        def init_saved_scores(self) -> None:
                """
                Load the high score from disk, or initialize to 0.
                """
                if self.path.exists() and self.path.stat().st_size > 0:
                    contents = self.path.read_text()
                    scores = json.loads(contents)
                    self.hi_score = scores.get('hi_score', 0)
                else:
                    self.hi_score = 0
                    self.save_scores()


        def save_scores(self) -> None:
                """
                Save the current high score to disk.
                """
                scores = {'hi_score': self.hi_score}
                contents = json.dumps(scores, indent=4)
                try:
                    self.path.write_text(contents)
                except FileNotFoundError as e:
                    print("File not found!:", e)


        def reset_stats(self) -> None:
                """
                Reset stats for a new game or life loss.
                """
                self.lives_left = self.settings.starting_lives
                self.score = 0
                self.wave = 1


        def update(self, collisions: dict[pygame.sprite.Sprite, list[pygame.sprite.Sprite]]) -> None:
                """
                Update the current score and high score after collisions.
                """
                self._update_score(collisions)
                self._update_hi_score()


        def _update_hi_score(self) -> None:
                """
                Update the high score if current score exceeds it.
                """
                if self.score > self.hi_score:
                    self.hi_score = self.score
                    self.save_scores()


        def _update_score(self, collisions: dict) -> None:
                """
                Add alien value to score for each collision.
                """
                for alien in collisions.values():
                    self.score += self.settings.alien_value


        def update_wave(self) -> None:
                """
                Increment the wave counter.
                """
                self.wave += 1
