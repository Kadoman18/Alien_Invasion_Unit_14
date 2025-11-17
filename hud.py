"""
Module providing UI/HUD rendering utilities.

Includes font caching, and UI helpers.
"""

import pygame

# Cache storing loaded font objects so fonts are not reloaded repeatedly
font_cache = {}

# Mapping of font keys to their font file paths
fonts = {
        'ss_reg': 'assets/fonts/silkscreen/silkscreen_regular.ttf',
        'ss_bold': 'assets/fonts/silkscreen/silkscreen_bold.ttf'
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
