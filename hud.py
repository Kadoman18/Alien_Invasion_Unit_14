"""
Module providing UI/HUD rendering utilities.

Includes panel/button management, font caching, and UI helpers for the Alien Invasion game.
"""
from pathlib import Path
import pygame
from typing import TYPE_CHECKING
from dataclasses import dataclass


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


@dataclass
class LabelData:
        """Holds the text label properties for HUD."""
        text: str
        text_size: int
        center: tuple[int, int]
        color: str | tuple[int, int, int]


@dataclass
class PanelData:
        """Holds the panel properties for HUD."""
        text: str
        center: tuple[int, int]
        text_size: int
        text_color: str | tuple[int, int, int]
        fill_color: str | tuple[int, int, int]
        border_color: str | tuple[int, int, int]
        pause_only: bool = False


class TextLabel:
        """
        Handles a single text label.
        """

        def __init__(self, game, data: LabelData, font_path: Path):
                self.game = game
                self.data = data
                self.settings = game.settings

                # Load font with caching
                font_key = Path(font_path).name
                if font_key not in self.settings.font_cache:
                        self.settings.font_cache[font_key] = {}
                if data.text not in self.settings.font_cache[font_key]:
                        self.settings.font_cache[font_key][data.text] = pygame.font.Font(font_path, data.text_size)
                self.font = self.settings.font_cache[font_key][data.text]

                # Render surface
                self.surface = self.font.render(data.text, False, data.color)
                self.rect = self.surface.get_rect(center=data.center)

        def set_text(self, text: str):
                self.data.text = text
                self.surface = self.font.render(text, False, self.data.color)
                self.rect = self.surface.get_rect(center=self.data.center)


class Panel:
        """
        Handles a panel with text overlay.
        """

        def __init__(self, game, data: PanelData, font_path: Path):
                self.game = game
                self.settings = game.settings
                self.data = data

                self.pause_only = data.pause_only

                # Create the text label
                label_data = LabelData(data.text, data.text_size, data.center, data.text_color)
                self.label = TextLabel(game, label_data, font_path)

                # Padding
                self.padding = (self.settings.screen_size[0] // 45, self.settings.screen_size[1] // 100)

                # Panel size
                self.panel_size = (self.label.rect.width + self.padding[0], self.label.rect.height + self.padding[1])
                self.surface = pygame.Surface(self.panel_size)

                # Fill panel
                fill_size = (int(self.panel_size[0] * 0.9), int(self.panel_size[1] * 0.9))
                fill_rect = pygame.Rect(0, 0, fill_size[0], fill_size[1])
                fill_rect.center = (self.panel_size[0] // 2, self.panel_size[1] // 2)
                self.surface.fill(data.border_color)
                self.surface.fill(data.fill_color, fill_rect)

                # Position rect
                self.rect = self.surface.get_rect(center=data.center)
                self.default_center = data.center


class HUD:
        """Main HUD management class."""

        def __init__(self, game: 'AlienInvasion') -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings
                self.stats = game.stats

                # Lifes icons (preload once)
                self.life_display_image = pygame.transform.scale(
                        pygame.image.load(self.settings.ship_image).convert_alpha(),
                        self.settings.life_display_icon_size
                )

                # Create HUD panels using dataclasses
                self.play_button = Panel(
                        game,
                        PanelData(
                                text=self.settings.play_button_text,
                                center=self.settings.play_button_loc,
                                text_size=self.settings.play_button_font_size,
                                text_color="white",
                                fill_color="green",
                                border_color="gray",
                                pause_only=True
                        ),
                        self.settings.play_button_font
                )

                self.pause_button = Panel(
                        game,
                        PanelData(
                                text=self.settings.pause_button_text,
                                center=self.settings.pause_button_loc,
                                text_size=self.settings.pause_button_font_size,
                                text_color="white",
                                fill_color="green",
                                border_color="gray",
                                pause_only=False
                        ),
                        self.settings.pause_button_font
                )

                # Create labels using dataclasses
                self.hi_score_display = TextLabel(
                        game,
                        LabelData(f"Hi-Score: {self.stats.hi_score}", self.settings.hi_score_size, self.settings.hi_score_loc, "white"),
                        self.settings.hi_score_font
                )

                self.score_display = TextLabel(
                        game,
                        LabelData(f"Score: {self.stats.score}", self.settings.score_size, self.settings.score_loc, "white"),
                        self.settings.score_font
                )

                self.wave_display = TextLabel(
                        game,
                        LabelData(f"Wave: {self.stats.wave}", self.settings.wave_size, self.settings.wave_loc, "white"),
                        self.settings.wave_font
                )

                self.panels = [self.play_button, self.pause_button]
                self.labels = [self.wave_display, self.score_display, self.hi_score_display]

        def draw(self, surface: pygame.Surface):
                """Draws all HUD elements on the screen."""

                # Update labels
                self.score_display.set_text(f"Score: {self.stats.score}")
                self.wave_display.set_text(f"Wave: {self.stats.wave}")
                self.hi_score_display.set_text(f"Hi-Score: {self.stats.hi_score}")

                # Draw lives
                lifeX, lifeY = self.settings.life_display_loc
                for life in range(0, self.stats.lives_left - 1):
                        rect = self.life_display_image.get_rect(
                                topleft=(lifeX + life * self.settings.life_display_padding, lifeY)
                        )
                        surface.blit(self.life_display_image, rect)

                # Draw the labels
                for label in self.labels:
                        surface.blit(label.surface, label.rect)

                # Draw the panels
                for panel in self.panels:
                        visible = (panel.pause_only and self.game.paused) or (not panel.pause_only and not self.game.paused)
                        if visible:
                                panel.rect.center = panel.default_center
                                surface.blit(panel.surface, panel.rect)

                                # Draw label in panel center
                                label_rect = panel.label.surface.get_rect(center=panel.surface.get_rect().center)
                                panel.surface.blit(panel.label.surface, label_rect)
                        else:
                                panel.rect.center = (-1000, -1000)
