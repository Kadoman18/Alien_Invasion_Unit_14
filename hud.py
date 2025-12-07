"""
Module providing UI/HUD rendering utilities.

Includes font caching, and UI helpers.
"""

from button import Button
from pathlib import Path
import pygame
from typing import TYPE_CHECKING


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class HUD:
        def __init__(self, game: 'AlienInvasion') -> None:

                self.game = game
                self.settings = game.settings

                # Create the play button
                self.play_button = Button(
                        self.settings.play_button_text,
                        self.settings.play_button_font,
                        ((self.settings.screen_size[0] - (self.settings.screen_size[0] // 2)),
                         (self.settings.screen_size[1] - (self.settings.screen_size[1] // 2))),
                        self.settings.screen_size[0] // 35,
                        "white",
                        "green",
                        "black",
                        True,
                        game
                        )
                
                # Define default play button location
                self.play_button_location = self.play_button.rect


        # TODO
        def wave(self) -> None:
                """
                Handles the wave increments and label.
                """

                # Increment the wave
                self.settings.wave += 1
