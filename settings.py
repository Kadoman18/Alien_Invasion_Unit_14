"""
Settings module defining global configuration for the Alien Invasion game.

Provides asset paths, screen size detection (with macOS adjustments), and global settings.
"""

import pygame
import platform
import paths
from pathlib import Path
from dataclasses import dataclass


class Settings:
        """
        Container for game-wide configuration values.

        Includes window title, computed screen size, asset paths,
        and dynamic values such as sprite scaling and FPS limits.
        """

        @dataclass
        class ScreenSize:
                """
                Represents the usable screen area for the game window.

                Notes
                -----
                • pygame reports the full display size, which on macOS includes
                  the menu bar (and sometimes the dock). A constant offset is
                  subtracted to ensure the window fits entirely within visible
                  space.

                • The values here are class attributes, meaning ScreenSize.x
                  and ScreenSize.y can be accessed without instantiating the class.
                """

                # Initialize pygame’s display module so desktop size can be queried
                pygame.display.init()

                # Easy Toggle for testing screen sizes and their effects on gameplay
                DEBUGGING: bool = False
                if DEBUGGING:
                        x: int = 900
                        y: int = 450
                else:
                        x: int = pygame.display.get_desktop_sizes()[0][0]
                        # Platform-specific vertical height adjustment
                        if platform.system() == 'Darwin':
                                # Subtract macOS menu bar height (approx. 61 px, at least on mine.. idk)
                                # This ensures the game window isn't pushed below the bottom of the screen
                                y: int = pygame.display.get_desktop_sizes()[0][1] - 61
                        else:
                                # Full height on Windows/Linux
                                y: int = pygame.display.get_desktop_sizes()[0][1]

        def __init__(self):
                """
                Initializes global settings
                """

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
                self.screen_size: tuple[int, int] = (
                        self.ScreenSize.x,
                        self.ScreenSize.y
                )

                #------- Play Button Settings -------
                self.play_button_text: str = "Play"
                self.play_button_font: Path = paths.Font.bold

                #------- Ship settings -------
                # Paths
                self.ship_image: Path = paths.Graphics.ship
                # Scale proportional to the screen size
                self.ship_size: tuple[int, int] = (
                        self.ScreenSize.x // 15,
                        self.ScreenSize.y // 10
                )

                # Set ships speed proportional to screen size
                self.ship_speed: int = self.ScreenSize.x // 150
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
                        self.ScreenSize.x // 60,
                        self.ScreenSize.y // 20
                )

                # Sets laser speed proportional to screen size
                self.laser_speed: int  = self.ScreenSize.x // 125

                #------- Alien Ship settings -------
                # Paths
                self.alien_image: Path = paths.Graphics.alien

                # Scale proportional to the screen size
                self.alien_size: tuple[int, int] = (
                        self.ScreenSize.x // 25,
                        self.ScreenSize.y // 15
                )

                #------- Horde Settings -------
                # Set horde speed proportional to screen size
                self.horde_speed: int = self.ScreenSize.x // 365

                # Set horde advance to alien height
                self.horde_advance: int = self.alien_size[1]

                # Dummy value for direction
                self.horde_direction: int = 1

                # Set horde padding proportional to screen size
                self.horde_padding: int = self.ScreenSize.x // 147

                # Set horde size (columns, rows)
                self.horde_size: tuple[int, int] = (6, 14)
