"""
Module providing UI/HUD rendering utilities.

Includes font caching, and UI helpers.
"""

import pygame
import paths
from pathlib import Path
from typing import Protocol

# Cache storing loaded font objects so fonts are not reloaded repeatedly
font_cache = {}

# Mapping of font keys to their font file paths
fonts = {
        'ss_reg': 'assets/fonts/Silkscreen/Silkscreen-Regular.ttf',
        'ss_bold': 'assets/fonts/Silkscreen/Silkscreen-Bold.ttf'
}


def text_label(text: str, font_key: str, size: int, color: str) -> pygame.Surface:
        """
        Render a text label using a cached pygame font.

        Parameters
        ----------
        text : str
                The text content to render.
        font_key : str
                A key referencing the font path in the `fonts` dictionary.
        size : int
                The pixel size of the font.
        color : str
                A pygame-compatible color value (name or RGB tuple).

        Returns
        -------
        pygame.Surface
                A rendered text surface ready to blit to the screen.
        """

        # Create font group in cache if missing
        if font_key not in font_cache:
                font_cache[font_key] = {}

        # Load the font at this size if not previously loaded
        if size not in font_cache[font_key]:
                font_cache[font_key][size] = pygame.font.Font(fonts[font_key], size)

        # Retrieve font from cache and render the text
        font = font_cache[font_key][size]
        return font.render(text, False, color)


def wave() -> str:
        """
        Handles the wave increments and label.

        Returns
        -------
        str
                A wave label in the format 'Wave: *n*'.

        Notes
        -----
        Currently always returns 1 because the wave system
        has not been implemented yet.
        """

        wave = 1
        return f'Wave: {wave}'

class HasSurfRect(Protocol):
        """
        Protocol defining the required attributes for game and HUD sprites.

        This protocol exists purely for static type checking (Pylance / Pyright)
        and ensures that any object passed around as a sprite provides the
        minimum properties that the game relies on:

        Attributes
        ----------
        surf : pygame.Surface
                The image surface used for rendering the sprite.
        rect : pygame.Rect
                The rectangle defining the sprite's position and size.

        Notes
        -----
        • pygame.sprite.Sprite does not guarantee the presence of `.surf`, and
          only optionally includes `.image` and `.rect`. Because this project uses
          `.surf` consistently (instead of `.image`), a custom protocol is needed
          so static type checkers know these attributes exist.

        • This protocol does not enforce inheritance from pygame.sprite.Sprite.
          Any object with `.surf` and `.rect` is considered valid, allowing both
          HUD elements and game entities to share a unified interface.

        • At runtime, Python does not check protocols; they only affect type
          checking and IDE autocomplete. No performance cost is added.
        """
        surf: pygame.Surface
        rect: pygame.Rect



def make_custom_sprite(
        path: Path,
        scale: tuple[int, int] | None = None
) -> HasSurfRect:
        """
        Create a pygame Sprite from an image file for HUD elements.

        Parameters
        ----------
        path : str | Path | PathLike[str]
                The file path of the image you want to load.
        scale : (int, int) or None
                Optional width/height scaling. If None, keeps original size.

        Returns
        -------
        pygame.sprite.Sprite
                A sprite with an surf and rect, ready to be drawn or added
                to a sprite group.
        """

        class CustomSprite(pygame.sprite.Sprite):
                def __init__(self, img_path: Path, img_scale: tuple[int, int] | None):
                        super().__init__()

                        # Load and convert image
                        surf = pygame.image.load(img_path).convert_alpha()

                        # Scale if requested
                        if img_scale is not None:
                                surf = pygame.transform.scale(surf, img_scale)

                        self.surf = surf
                        self.rect = self.surf.get_rect()

        sprite = CustomSprite(path, scale)
        return sprite