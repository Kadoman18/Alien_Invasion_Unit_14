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

                # Create the play button
                self.play_button = Panel(
                        self.settings.play_button_text,
                        self.settings.play_button_font,
                        self.settings.play_button_loc,
                        self.settings.play_button_font_size,
                        "white",
                        "green",
                        "gray",
                        True,
                        game
                        )

                # Create the pause button
                self.pause_button = Panel(
                        self.settings.pause_button_text,
                        self.settings.pause_button_font,
                        self.settings.pause_button_loc,
                        self.settings.pause_button_font_size,
                        "white",
                        "green",
                        "gray",
                        False,
                        game
                        )

                self.panels = [self.play_button, self.pause_button]

        # TODO
        def wave(self) -> None:
                """
                Handles the wave increments and label.
                """

                # Increment the wave
                self.settings.wave += 1


class Panel:
        """
        A UI panel class for pygame applications.

        This class creates a customizable panel with text, border, and fill colors.
        The panel can be positioned at a specified point and supports rendering
        onto pygame surfaces.
        """

        # Initialize local variables
        def __init__(
                        self,
                        text: str,
                        font: Path,
                        center: tuple[int, int],
                        text_size: int,
                        text_color: str | tuple[int, int, int],
                        fill_color: str | tuple[int, int, int],
                        border_color: str | tuple[int, int, int],
                        pause_only: bool,
                        game: 'AlienInvasion'
                        ) -> None:

                # Import game reference and settings
                self.game = game
                self.settings = game.settings

                # Render label
                self.label: pygame.Surface = self.text_label(text, font, text_size, text_color)

                # Get label size for sizing panel
                self.label_size = self.label.get_size()

                # State of the game
                self.pause_only = pause_only

                # Padding between text and panel edges
                self.padding: tuple[int, int] = (
                        (self.settings.screen_size[0] // 45),
                        (self.settings.screen_size[1] // 100)
                        )

                # Set panel size based on label size and create the surface
                self.panel_size: tuple[int, int] = (
                        self.label_size[0] + self.padding[0], self.label_size[1] + self.padding[1]
                        )
                self.panel: pygame.Surface = pygame.Surface(self.panel_size)

                # Compute fill in local panel coordinates
                fill_size: tuple[int, int] = (
                        int(self.panel_size[0] * 0.9),
                        int(self.panel_size[1] * 0.9)
                        )
                fill_rect = pygame.Rect(0, 0, fill_size[0], fill_size[1])
                fill_rect.center = (self.panel_size[0] // 2, self.panel_size[1] // 2)

                self.panel.fill(border_color)
                self.panel.fill(fill_color, fill_rect)

                # Create rect positioned at given location
                self.default_center = center
                self.rect: pygame.Rect = self.panel.get_rect(center=self.default_center)


        def text_label(
                        self,
                        text: str,
                        font_path: Path,
                        size: int,
                        color: str | tuple[int, int, int]
                        ) -> pygame.Surface:
                """
                Render a text label using a cached pygame font.

                Parameters
                ----------
                text : str
                        The text content to render.
                font_path : Path
                        A pathlib Path object to the font file.
                size : int
                        The pixel size of the font.
                color : str
                        A pygame-compatible color value (name or RGB tuple).

                Returns
                -------
                pygame.Surface
                        A rendered text surface ready to blit to the screen.
                """
                # Extract the fonts name
                font_key = Path(font_path).name

                # Create font group in cache if missing
                if font_key not in self.settings.font_cache:
                        self.settings.font_cache[font_key] = {}

                # Load the font at this size if not previously loaded
                if size not in self.settings.font_cache[font_key]:
                        self.settings.font_cache[font_key][size] = pygame.font.Font(font_path, size)

                # Retrieve font from cache and render the text
                font = self.settings.font_cache[font_key][size]
                return font.render(text, False, color)


        def draw(self, surface, paused) -> None:

                # Determine panel visibility based on pause state
                visible = (self.pause_only and paused) or (not self.pause_only and not paused)

                if visible:
                        # Restore original location
                        if self.rect.center != self.default_center:
                                self.rect.center = self.default_center

                        # Draw panel
                        surface.blit(self.panel, self.rect)

                        # Move the labels rect into place
                        label_rect = self.label.get_rect(center=self.panel.get_rect().center)

                        # Draw the label
                        self.panel.blit(self.label, label_rect)

                else:
                        # Move off-screen
                        self.rect.center = (-1000, -1000)


