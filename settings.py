"""
Settings module defining global configuration for the Alien Invasion game.

Provides screen size detection (with macOS adjustments) and access to
background asset paths.
"""

from dataclasses import dataclass
from pathlib import Path
import paths
import platform
import pygame


class Settings:
        """
        Container for game-wide configuration values.

        Includes window title, computed screen size, asset paths,
        and dynamic values such as ship scaling and FPS limits.
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
                Initialize global settings including:

                - window title
                - app icon
                - final screen size tuple used by pygame
                - calculated ship size scaling
                - background and icon asset paths
                - ship speed
                - FPS cap
                """

                # Title that appears in the window bar
                self.name: str = '👾 Alien Invasion 👾'

                # Icon path for pygame window
                self.icon: Path = paths.Graphics.icon

                # Convert ScreenSize class attributes into a tuple for pygame
                self.screen_size: tuple[int, int] = (
                        self.ScreenSize.x,
                        self.ScreenSize.y
                )

                # Background image path
                self.background: Path = paths.Graphics.background

                # Ship sprite scaling is proportional to the screen size, ensuring continuity across devices
                self.ship_size: tuple[int, int] = (
                        self.ScreenSize.x // 15,
                        self.ScreenSize.y // 10
                )

                # Sets ships speed proportional to screen size, ensuring continuity across devices
                self.ship_speed: int = self.ScreenSize.x // 150
                self.ship_base_firing_speed: int = self.ship_speed - (self.ship_speed // 3)
                self.ship_rapid_firing_speed: int = self.ship_speed // 2

                # Fire rate for continuous ship fire
                self.ship_base_fire_rate: int = 750
                self.ship_rapid_fire_rate: int = 250

                # Laser sprite scaling is proportional to the screen size, ensuring continuity across devices
                self.laser_size: tuple[int, int] = (
                        self.ScreenSize.x // 60,
                        self.ScreenSize.y // 20
                )

                # Sets laser speed proportional to screen size, ensuring continuity across devices
                self.laser_speed: int  = self.ScreenSize.x // 125

                # Path to laser fire noise
                self.laser_noise: Path = paths.Audio.laser

                # Sizing for the alien ship sprites
                self.alien_size: tuple[int, int] = (
                        self.ScreenSize.x // 25,
                        self.ScreenSize.y // 15
                )

                # Sets enemy speed proportional to screen size, ensuring continuity across devices
                self.alien_speed: int  = self.ScreenSize.x // 250

                # Frames per second cap for the main loop
                self.fps: int = 60
