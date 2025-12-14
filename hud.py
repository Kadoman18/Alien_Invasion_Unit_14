"""
Module providing UI/HUD rendering utilities.

Includes panel/button management, font caching, and UI helpers for the Alien Invasion game.
"""
from pathlib import Path
import pygame
from game_stats import GameStats
from typing import TYPE_CHECKING


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class HUD:
        def __init__(self, game: 'AlienInvasion') -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings
                self.stats = GameStats(self.game)

                # Create the play button
                self.play_button = Panel(
                        self.game,
                        self.settings.play_button_text,
                        self.settings.play_button_font,
                        self.settings.play_button_loc,
                        self.settings.play_button_font_size,
                        "white",
                        "green",
                        "gray",
                        True
                        )

                # Create the pause button
                self.pause_button = Panel(
                        self.game,
                        self.settings.pause_button_text,
                        self.settings.pause_button_font,
                        self.settings.pause_button_loc,
                        self.settings.pause_button_font_size,
                        "white",
                        "green",
                        "gray",
                        False
                        )
                
                # Hi Score display
                self.score_display = TextLabel(
                        self.game, f"Score: {self.stats.score}", self.settings.score_font, 20, "white"
                )

                self.panels = [self.play_button, self.pause_button]
                self.labels = [self.score_display]

class TextLabel:
        """
        Handles a single text label.
        """

        def __init__(self, game, text: str, font_path: Path, size: int, color: str | tuple[int, int, int]):
                self.game = game
                self.settings = game.settings
                self.text = text
                self.color = color

                # Load font with caching
                font_key = Path(font_path).name
                if font_key not in self.settings.font_cache:
                        self.settings.font_cache[font_key] = {}
                if size not in self.settings.font_cache[font_key]:
                        self.settings.font_cache[font_key][size] = pygame.font.Font(font_path, size)
                self.font = self.settings.font_cache[font_key][size]

                # Render surface
                self.surface = self.font.render(text, False, color)
                self.rect = self.surface.get_rect()

        def draw(self, surface: pygame.Surface, center: tuple[int, int]):
                if center:
                        self.rect.center = center
                surface.blit(self.surface, self.rect)


class Panel:
        """
        Handles a panel with text overlay.
        """

        def __init__(
                        self,
                        game,
                        text: str,
                        font_path: Path,
                        center: tuple[int, int],
                        text_size: int,
                        text_color: str | tuple[int, int, int],
                        fill_color: str | tuple[int, int, int],
                        border_color: str | tuple[int, int, int],
                        pause_only: bool = False
                        ):
                self.game = game
                self.settings = game.settings
                self.pause_only = pause_only

                # Create the text label
                self.label = TextLabel(game, text, font_path, text_size, text_color)

                # Padding
                self.padding = (self.settings.screen_size[0] // 45, self.settings.screen_size[1] // 100)

                # Panel size
                self.panel_size = (self.label.rect.width + self.padding[0], self.label.rect.height + self.padding[1])
                self.surface = pygame.Surface(self.panel_size)

                # Fill panel
                fill_size = (int(self.panel_size[0] * 0.9), int(self.panel_size[1] * 0.9))
                fill_rect = pygame.Rect(0, 0, fill_size[0], fill_size[1])
                fill_rect.center = (self.panel_size[0] // 2, self.panel_size[1] // 2)
                self.surface.fill(border_color)
                self.surface.fill(fill_color, fill_rect)

                # Position rect
                self.rect = self.surface.get_rect(center=center)
                self.default_center = center

        def draw(self, surface: pygame.Surface, paused: bool = False):
                # Show only if pause_only matches pause state
                visible = (self.pause_only and paused) or (not self.pause_only and not paused)
                if visible:
                        self.rect.center = self.default_center
                        surface.blit(self.surface, self.rect)

                        # Draw label in panel center
                        label_rect = self.label.surface.get_rect(center=self.surface.get_rect().center)
                        self.surface.blit(self.label.surface, label_rect)
                else:
                        # Move offscreen if hidden
                        self.rect.center = (-1000, -1000)