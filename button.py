"""
Button module for Alien Invasion game.

This module provides a Button class for creating clickable buttons in pygame applications.
Buttons support customizable text, colors, and positioning.
"""

from pathlib import Path
import pygame
from typing import TYPE_CHECKING


# Forward reference to avoid circular imports at runtime
if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class Button:
        """
        A clickable button class for pygame applications.

        This class creates a customizable button with text, border, and fill colors.
        The button can be positioned at a specified point and supports rendering
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

                # Get label size for sizing button size
                self.label_size = self.label.get_size()

                # State of the game
                self.pause_only = pause_only

                # Padding between text and button edges
                self.padding: int = (self.settings.screen_size[0] // 100)

                # Set button size based on label size
                self.button_size: tuple[int, int] = (self.label_size[0] + self.padding, self.label_size[1] + self.padding)
                self.fill_rect: pygame.Rect = pygame.Rect(4, 4, self.button_size[0] - 8, self.button_size[1] - 8)

                # Create button surface using calculated size
                self.button: pygame.Surface = pygame.Surface((self.button_size))

                # Fill button with border color, fill smaller area inside with fill color
                self.button.fill(border_color)
                self.button.fill(fill_color, self.fill_rect)

                # Create rect positioned at given location
                self.rect: pygame.Rect = self.button.get_rect(center=center)


        def text_label(self, text: str, font_path: Path, size: int, color: str | tuple[int, int, int]) -> pygame.Surface:
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
                """
                Renders the button and its label onto the given surface.

                This method blits the button image onto the provided surface at its
                predefined rect position, then centers and blits the label text on top
                of the button.

                Args:
                        surface: The pygame Surface object to draw the button onto.

                Returns:
                        None
                """
                if self.pause_only and paused:
                        # Draw button at its rect
                        surface.blit(self.button, self.rect)

                        # Center the label inside the button
                        label_rect = self.label.get_rect(center=self.button.get_rect().center)

                        # Blit label inside the button
                        self.button.blit(self.label, label_rect)

                if not self.pause_only and not paused:
                        # Draw button at its rect
                        surface.blit(self.button, self.rect)

                        # Center the label inside the button
                        label_rect = self.label.get_rect(center=self.button.get_rect().center)

                        # Blit label inside the button
                        self.button.blit(self.label, label_rect)
