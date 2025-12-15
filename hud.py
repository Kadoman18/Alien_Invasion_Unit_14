"""
Module providing UI/HUD rendering utilities.

Includes panel/button management, font caching, and UI helpers for the Alien Invasion game.
"""
from pathlib import Path
import pygame
from typing import TYPE_CHECKING


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class HUD:
        def __init__(self, game: 'AlienInvasion') -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings
                self.stats = game.stats

                # Lifes icons
                self.life_display_image = pygame.image.load(self.settings.ship_image).convert_alpha()
                self.life_display_image = pygame.transform.scale(self.life_display_image, self.settings.life_display_icon_size)

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
                self.hi_score_display = TextLabel(
                        self.game,
                        f"Hi-Score: {self.stats.hi_score}",
                        self.settings.hi_score_font,
                        self.settings.hi_score_size,
                        self.settings.hi_score_loc,
                        "white"
                )

                # Score display
                self.score_display = TextLabel(
                        self.game,
                        f"Score: {self.stats.score}",
                        self.settings.score_font,
                        self.settings.score_size,
                        self.settings.score_loc,
                        "white"
                )

                # Waves display
                self.wave_display = TextLabel(
                        self.game,
                        f"Wave: {self.stats.wave}",
                        self.settings.wave_font,
                        self.settings.wave_size,
                        self.settings.wave_loc,
                        "white"
                )

                self.panels = [self.play_button, self.pause_button]
                self.labels = [self.wave_display, self.score_display, self.hi_score_display]

        def draw(self, surface: pygame.Surface):
                self.score_display.set_text(f"Score: {self.stats.score}")
                self.wave_display.set_text(f"Wave: {self.stats.wave}")
                self.hi_score_display.set_text(f"Hi-Score: {self.stats.hi_score}")

                # Draw lives
                lifeX, lifeY = self.settings.life_display_loc
                for life in range(self.stats.lives_left):
                        rect = self.life_display_image.get_rect(topleft=(lifeX + life * self.settings.life_display_padding, lifeY))
                        surface.blit(self.life_display_image, rect)
                # Draw the labels
                for label in self.labels:
                        surface.blit(label.surface, label.rect)

                # Draw the panels
                for panel in self.panels:
                        # Show only if pause_only matches pause state
                        visible = (panel.pause_only and self.game.paused) or (not panel.pause_only and not self.game.paused)
                        if visible:
                                panel.rect.center = panel.default_center
                                surface.blit(panel.surface, panel.rect)

                                # Draw label in panel center
                                label_rect = panel.label.surface.get_rect(center=panel.surface.get_rect().center)
                                panel.surface.blit(panel.label.surface, label_rect)
                        else:
                                # Move offscreen if hidden
                                panel.rect.center = (-1000, -1000)


class TextLabel:
        """
        Handles a single text label.
        """

        def __init__(self, game, text: str, font_path: Path, size: int, center: tuple[int, int], color: str | tuple[int, int, int]):
                self.game = game
                self.text = text
                self.center = center
                self.color = color
                self.settings = game.settings

                # Load font with caching
                font_key = Path(font_path).name
                if font_key not in self.settings.font_cache:
                        self.settings.font_cache[font_key] = {}
                if size not in self.settings.font_cache[font_key]:
                        self.settings.font_cache[font_key][size] = pygame.font.Font(font_path, size)
                self.font = self.settings.font_cache[font_key][size]

                # Render surface
                self.surface = self.font.render(text, False, color)
                self.rect = self.surface.get_rect(center = self.center)

        def set_text(self, text: str):
                self.text = text
                self.surface = self.font.render(text, False, self.color)
                self.rect = self.surface.get_rect(center = self.center)


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
                self.label = TextLabel(game, text, font_path, text_size, center,  text_color)

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