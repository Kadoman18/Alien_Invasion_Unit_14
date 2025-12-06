import pygame
from hud import text_label
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion

class Button:

        def __init__(
                        self,
                        text: str,
                        font: Path,
                        center: tuple[int, int],
                        text_size: int,
                        text_color: str | tuple[int, int, int],
                        fill_color: str | tuple[int, int, int],
                        border_color: str | tuple[int, int, int],
                        game: 'AlienInvasion'
                        ) -> None:

                self.game = game
                self.settings = game.settings

                # Render label
                self.label: pygame.Surface = text_label(text, font, text_size, text_color)

                # Get label size for sizing button size
                self.label_size = self.label.get_size()

                # Padding between text and button edges
                self.padding: int = (self.game.screen_rect[0] // 200)

                # Set button size based on label size
                self.button_size: tuple[int, int] = (self.label_size[0] + self.padding, self.label_size[1] + self.padding)
                self.fill_rect: pygame.Rect = pygame.Rect(4, 4, self.button_size[0] - 8, self.button_size[1] - 8)

                # Create button surface using calculated size
                self.button: pygame.Surface = pygame.Surface((self.button_size))
                self.button.fill(border_color)
                self.button.fill(fill_color, self.fill_rect)

                # Create rect positioned at given location
                self.rect: pygame.Rect = self.button.get_rect(center=center)

        def draw(self, surface):
                # Draw button at its rect
                surface.blit(self.button, self.rect)

                # Center the label inside the button
                label_rect = self.label.get_rect(center=self.button.get_rect().center)

                # Blit label inside the button
                self.button.blit(self.label, label_rect)
