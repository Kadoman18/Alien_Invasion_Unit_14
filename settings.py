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

                # Horizontal screen width (same on all platforms)
                x: int = pygame.display.get_desktop_sizes()[0][0]

                # DEBUGGING OPTION:
                # x: int = 900

                # Platform-specific vertical height adjustment
                if platform.system() == 'Darwin':
                        # Subtract macOS menu bar height (approx. 61 px)
                        # This ensures the game window isn't covered by the menu bar
                        y: int = pygame.display.get_desktop_sizes()[0][1] - 61

                        # DEBUGGING OPTION:
                        # y: int = 450
                else:
                        # Full height on Windows/Linux
                        y: int = pygame.display.get_desktop_sizes()[0][1]

        def __init__(self):
                """
                Initialize global settings including:

                • window title
                • final screen size tuple used by pygame
                • calculated ship size scaling
                • background and icon asset paths
                • FPS cap
                """

                # Title that appears in the window bar
                self.name: str = '👾 Alien Invasion 👾'

                # Convert ScreenSize class attributes into a tuple for pygame
                self.screen_size: tuple[int, int] = (
                        self.ScreenSize.x,
                        self.ScreenSize.y
                )

                # Background image path (Path object from paths.Graphics)
                self.background: Path = paths.Graphics.background

                # Ship sprite scaling is proportional to the screen size
                self.ship_size: tuple[int, int] = (
                        self.ScreenSize.x // 15,
                        self.ScreenSize.y // 10
                )

                # Icon path for pygame window (if used)
                self.icon: Path = paths.Graphics.icon

                # Frames per second cap for the main loop
                self.fps: int = 60
