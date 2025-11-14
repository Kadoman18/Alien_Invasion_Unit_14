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

        Includes window title, computed screen size, and background
        resource paths. Screen size detection accounts for macOS menu
        bar height to obtain usable space.
        """

        @dataclass
        class ScreenSize:
                """
                Defines the usable screen width and height for the game window.

                On macOS, pygame reports the total display height including
                the menu bar. To compensate, this class subtracts a constant
                offset so the created window fits entirely on-screen without
                overlapping the menu bar.

                On all other platforms, the full desktop size is used.
                """

                pygame.display.init()
                x: int = pygame.display.get_desktop_sizes()[0][0]
                if platform.system() == 'Darwin':
                        y: int = pygame.display.get_desktop_sizes()[0][1] - 61
                else:
                        y: int = pygame.display.get_desktop_sizes()[0][1]

        def __init__(self):
                """
                Initialize settings including game name, calculated screen size,
                and the path to the background image asset.
                """
                self.name: str = '👾 Alien Invasion 👾'

                self.screen_size: tuple[int, int] = (
                        self.ScreenSize().x,
                        self.ScreenSize().y
                )

                self.background: Path = paths.Graphics().background
