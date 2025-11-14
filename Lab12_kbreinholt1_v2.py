"""
Module providing text rendering utilities and the main Alien Invasion
game loop using pygame. Includes font caching, UI helpers, and the core
game window initialization.
"""

import pygame
import settings
import paths


font_cache = {}
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

        if font_key not in font_cache:
                font_cache[font_key] = {}

        if size not in font_cache[font_key]:
                font_cache[font_key][size] = pygame.font.Font(fonts[font_key], size)

        font = font_cache[font_key][size]
        return font.render(text, False, color)


def wave() -> str:
        """
        Generate a formatted wave display string.

        Returns
        -------
        str
                A wave label in the format 'Wave: *number*'.
        """

        wave = 1
        return f'Wave: {wave}'


class AlienInvasion:
        """
        Main game controller for the Alien Invasion application.

        Handles initialization of pygame, screen setup, background loading,
        and the primary game loop.
        """

        def __init__(self):
                """
                Initialize game settings, window, background, and runtime systems.
                """
                pygame.init()
                self.settings = settings.Settings()

                # Initialize screen using configured dimensions
                self.screen = pygame.display.set_mode((self.settings.screen_size))
                pygame.display.set_caption(self.settings.name)

                # Load background surface
                self.sky_surf = pygame.image.load(self.settings.background)

                self.running = True
                self.clock = pygame.time.Clock()

        def run_game(self) -> None:
                """
                Execute the main game loop until the window is closed.
                """
                while self.running:
                        # Event processing
                        for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                        self.running = False
                                        pygame.quit()
                                        exit()

                        # Draw background and update display
                        self.screen.blit(self.sky_surf, (0, 0))
                        pygame.display.flip()

                        # Cap framerate
                        self.clock.tick(60)


if __name__ == '__main__':
        AlienInvasion().run_game()
