"""
Settings module defining global configuration for the Alien Invasion game.

Provides asset paths, screen size detection (with macOS adjustments), and global settings.
"""

from pathlib import Path
import paths
import platform
import pygame


class Settings:
        """
        Container for game-wide configuration values.

        Includes window title, computed screen size, asset paths,
        and dynamic values such as sprite scaling and FPS limits.
        """

        # Initialize local variables for import and global use
        def __init__(self):
                """
                Initializes global settings
                """

                # Easy Toggle for testing screen sizes and their effects on gameplay
                self.DEBUGGING: bool = False

                #------- General Settings
                # Title that appears in the window bar
                self.name: str = '👾 Alien Invasion 👾'

                # Icon path for pygame window
                self.icon: Path = paths.Graphics.icon

                # Background image path
                self.background: Path = paths.Graphics.background

                # Frames per second cap for the main loop
                self.fps: int = 60

                # Convert ScreenSize class attributes into a tuple for pygame
                self.screen_size: tuple[int, int] = self.ScreenSize()

                # Cache storing loaded font objects
                self.font_cache: dict = {}

                # Mapping of font keys to their font file paths
                self.fonts: dict = {
                        'ss_reg': 'assets/fonts/silkscreen/silkscreen_regular.ttf',
                        'ss_bold': 'assets/fonts/silkscreen/silkscreen_bold.ttf'
}
                # Dummy variable for wave counter (not done yet)
                self.wave: int = 1

                #------- Button Settings -------
                self.play_button_text: str = "Play"
                self.play_button_font: Path = paths.Font.bold
                self.play_button_font_size: int = self.screen_size[0] // 35
                self.play_button_loc: tuple[int, int] = (
                        (self.screen_size[0] - (self.screen_size[0] // 2)),
                        (self.screen_size[1] - (self.screen_size[1] // 2))
                        )

                self.pause_button_text: str = "||"
                self.pause_button_font: Path = paths.Font.bold
                self.pause_button_font_size: int = self.screen_size[0] // 60
                self.pause_button_loc: tuple[int, int] = (
                        self.screen_size[0] - (self.screen_size[0] // 25),
                        int(self.screen_size[1] * 0.06)
                        )

                #------- Ship settings -------
                # Paths
                self.ship_image: Path = paths.Graphics.ship
                # Scale proportional to the screen size
                self.ship_size: tuple[int, int] = (
                        self.screen_size[0] // 15,
                        self.screen_size[1] // 10
                )

                # Set ships speed proportional to screen size
                self.ship_speed: int = self.screen_size[0] // 150
                self.ship_wrap_buffer: int = 25

                # Ships speed modifiers depending on firing mode
                self.ship_base_firing_speed: int = self.ship_speed - (self.ship_speed // 3)
                self.ship_rapid_firing_speed: int = self.ship_speed // 2

                # Fire rate for continuous ship fire
                self.ship_base_fire_rate: int = 750
                self.ship_rapid_fire_rate: int = 250

                #------- Laser Settings -------
                # Paths
                self.laser_graphic: Path = paths.Graphics.laser
                self.laser_noise: Path = paths.Audio.laser
                self.impact_noise: Path = paths.Audio.impact

                # Scale proportional to the screen size
                self.laser_size: tuple[int, int] = (
                        self.screen_size[0] // 60,
                        self.screen_size[1] // 20
                )

                # Sets laser speed proportional to screen size
                self.laser_speed: int  = self.screen_size[0] // 125

                #------- Alien Ship settings -------
                # Paths
                self.alien_image: Path = paths.Graphics.alien

                # Scale proportional to the screen size
                self.alien_size: tuple[int, int] = (
                        self.screen_size[0] // 25,
                        self.screen_size[1] // 15
                )

                #------- Horde Settings -------
                # Debugging option
                if self.DEBUGGING:

                        # Set horde speed proportional to screen size
                        self.horde_speed: int = self.screen_size[0] // 121

                        # Set horde size (columns, rows)
                        self.horde_size: tuple[int, int] = (2, 14)
                else:

                        # Set horde speed proportional to screen size
                        self.horde_speed: int = self.screen_size[0] // 365

                        # Set horde size (columns, rows)
                        self.horde_size: tuple[int, int] = (6, 14)

                # Set horde advance to alien height
                self.horde_advance: int = self.alien_size[1]

                # Dummy value for direction
                self.horde_direction: int = 1

                # Set horde padding proportional to screen size
                self.horde_padding: int = self.screen_size[0] // 147


        def ScreenSize(self):
                """
                Represents the usable screen area for the game window.

                Note

                • pygame reports the full display size, which on macOS includes
                  the menu bar (and sometimes the dock). A constant offset is
                  subtracted to ensure the window fits entirely within visible
                  space.
                """

                # Initialize pygame's display module so desktop size can be queried
                pygame.display.init()

                if self.DEBUGGING:
                        self.x: int = 900
                        self.y: int = 450
                else:
                        self.x: int = pygame.display.get_desktop_sizes()[0][0]
                        # Platform-specific vertical height adjustment
                        if platform.system() == 'Darwin':
                                # Subtract macOS menu bar height (approx. 61 px, at least on mine.. idk)
                                # This ensures the game window isn't pushed below the bottom of the screen
                                self.y: int = pygame.display.get_desktop_sizes()[0][1] - 61
                        else:
                                # Full height on Windows/Linux
                                self.y: int = pygame.display.get_desktop_sizes()[0][1]

                return (self.x, self.y)
