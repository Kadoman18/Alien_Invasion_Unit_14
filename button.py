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
                        game: 'AlienInvasion'
                        ) -> None:

                self.game = game
                self.settings = game.settings

                # Render label
                self.label: pygame.Surface = text_label(text, font, text_size, text_color)

                # Get label size for sizing button size
                label_size = self.label.get_size()

                # Padding between text and button edges
                padding: int = (self.game.screen_rect[0] // 200) * 2

                # Set button size based on label size
                button_size: tuple[int, int] = (label_size[0] + padding, label_size[1] + padding)

                # Create button surface using calculated size
                self.button: pygame.Surface = pygame.Surface((button_size))
                self.button.fill(fill_color)

                # Create rect positioned at given location
                self.rect: pygame.Rect = self.button.get_rect(center=center)


        def draw(self, surface):
                # Draw button at its rect
                surface.blit(self.button, self.rect)

                # Center the label inside the button
                label_rect = self.label.get_rect(center=self.button.get_rect().center)

                # Blit label inside the button
                self.button.blit(self.label, label_rect)
