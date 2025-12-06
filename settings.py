"""
Settings module defining global configuration for the Alien Invasion game.

Provides asset paths, screen size detection (with macOS adjustments), and global settings.
"""

import pygame
from pathlib import Path
from dataclasses import dataclass
import platform


ROOT = Path.cwd() / 'assets'


@dataclass
class Audio:
        """
        File paths for all audio resources used by the game.

        Attributes
        ----------
        impact : Path
                Path to the player impact sound effect.
        laser : Path
                Path to the laser firing sound effect.
        """
        impact: Path = ROOT / "audio" / "impact.mp3"
        laser: Path = ROOT / "audio" / "laser.mp3"


@dataclass
class File:
        """
        File paths for data and JSON-based persistent storage.

        Attributes
        ----------
        scores : Path
                Path to the JSON file storing player score data.
        """
        scores: Path = ROOT / "file" / "scores.json"


@dataclass
class Font:
        """
        File paths for all font resources used in rendering UI text.

        Attributes
        ----------
        bold : Path
                Path to the bold silkscreen font.
        regular : Path
                Path to the regular silkscreen font.
        """
        bold: Path = ROOT / "fonts" / "silkscreen" / "silkscreen_bold.ttf"
        regular: Path = ROOT / "fonts" / "silkscreen" / "silkscreen_regular.ttf"


@dataclass
class Graphics:
        """
        File paths for all graphical assets, including sprites, UI elements,
        and backgrounds.

        Attributes
        ----------
        asteroid : Path
                Asteroid sprite asset.
        beams : Path
                Beam graphics asset.
        alien : Path
                Alien ship sprite.
        laser : Path
                Laser blast sprite.
        ship : Path
                Primary player ship sprite.
        background : Path
                Primary game background image.
        icon : Path
                App icon image.
        """
        asteroid: Path = ROOT / "graphics" / "asteroid.png"
        beams: Path = ROOT / "graphics" / "beams.png"
        alien: Path = ROOT / "graphics" / "alien.png"
        laser: Path = ROOT / "graphics" / "laser.png"
        ship: Path = ROOT / "graphics" / "ship.png"
        background: Path = ROOT / "graphics" / "background.png"
        icon: Path = ROOT / "graphics" / "icon.png"


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
                Initializes global settings
                """

                #------- General Settings
                # Title that appears in the window bar
                self.name: str = '👾 Alien Invasion 👾'

                # Icon path for pygame window
                self.icon: Path = Graphics.icon

                # Background image path
                self.background: Path = Graphics.background

                # Frames per second cap for the main loop
                self.fps: int = 60

                # Convert ScreenSize class attributes into a tuple for pygame
                self.screen_size: tuple[int, int] = (
                        self.ScreenSize.x,
                        self.ScreenSize.y
                )

                #------- Play Button Settings -------
                self.play_button_text: str = "Play"
                self.play_button_font: Path = Font.bold

                #------- Ship settings -------
                # Scale proportional to the screen size
                self.ship_size: tuple[int, int] = (
                        self.ScreenSize.x // 15,
                        self.ScreenSize.y // 10
                )

                # Set ships speed proportional to screen size
                self.ship_speed: int = self.ScreenSize.x // 150

                # Ships speed modifiers depending on firing mode
                self.ship_base_firing_speed: int = self.ship_speed - (self.ship_speed // 3)
                self.ship_rapid_firing_speed: int = self.ship_speed // 2

                # Fire rate for continuous ship fire
                self.ship_base_fire_rate: int = 750
                self.ship_rapid_fire_rate: int = 250

                #------- Laser Settings -------
                # Paths
                self.laser_graphic = Graphics.laser
                self.laser_noise: Path = Audio.laser

                # Scale proportional to the screen size
                self.laser_size: tuple[int, int] = (
                        self.ScreenSize.x // 60,
                        self.ScreenSize.y // 20
                )

                # Sets laser speed proportional to screen size
                self.laser_speed: int  = self.ScreenSize.x // 125

                #------- Alien Ship settings -------
                # Paths
                self.alien_image: Path = Graphics.alien

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
