"""
Button module for Alien Invasion game.

This module provides a Button class for creating clickable buttons in pygame applications.
Buttons support customizable text, colors, and positioning.
"""

from hud import text_label
from pathlib import Path
from typing import TYPE_CHECKING
import pygame


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
                self.label: pygame.Surface = text_label(text, font, text_size, text_color)

                # Get label size for sizing button size
                self.label_size = self.label.get_size()

                # State of the game
                self.pause_only = pause_only

                # Padding between text and button edges
                self.padding: int = (self.game.screen_rect.width // 100)

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
