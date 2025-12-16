"""
Settings module defining global configuration for the Alien Invasion game.

Provides asset paths, screen size detection (with macOS adjustments), and global settings.
"""
from dataclasses import dataclass, field
from pathlib import Path
import paths
import platform
import pygame
from typing import Tuple, Dict


@dataclass
class Settings:
        """
        Container for game-wide configuration values.

        Includes window title, computed screen size, asset paths,
        and dynamic values such as sprite scaling and FPS limits.
        """

        DEBUGGING: bool = False

        # General Settings
        name: str = '👾 Alien Invasion 👾'
        icon: Path = paths.Graphics.icon
        background: Path = paths.Graphics.background
        fps: int = 60

        # Computed after init
        screen_size: Tuple[int, int] = field(init=False)
        font_cache: Dict[str, Dict[int, pygame.font.Font]] = field(default_factory=dict)
        fonts: Dict[str, str] = field(default_factory=lambda: {
                'ss_reg': 'assets/fonts/silkscreen/silkscreen_regular.ttf',
                'ss_bold': 'assets/fonts/silkscreen/silkscreen_bold.ttf'
        })

        # UI / GUI Settings
        hi_score_file: Path = paths.File.scores
        hi_score_font: Path = paths.Font.regular
        hi_score_size: int = field(init=False)
        hi_score_loc: Tuple[int, int] = field(init=False)

        score_file: Path = paths.File.scores
        score_font: Path = paths.Font.regular
        score_size: int = field(init=False)
        score_loc: Tuple[int, int] = field(init=False)

        wave_font: Path = paths.Font.regular
        wave_size: int = field(init=False)
        wave_loc: Tuple[int, int] = field(init=False)

        play_button_text: str = "Play"
        play_button_font: Path = paths.Font.bold
        play_button_font_size: int = field(init=False)
        play_button_loc: Tuple[int, int] = field(init=False)

        pause_button_text: str = "||"
        pause_button_font: Path = paths.Font.bold
        pause_button_font_size: int = field(init=False)
        pause_button_loc: Tuple[int, int] = field(init=False)

        # Ship settings
        ship_image: Path = paths.Graphics.ship
        ship_size: Tuple[int, int] = field(init=False)
        life_display_icon_size: Tuple[int, int] = field(init=False)
        life_display_padding: int = field(init=False)
        life_display_loc: Tuple[int, int] = field(init=False)
        starting_lives: int = 3
        ship_speed: int = field(init=False)
        ship_wrap_buffer: int = 25
        ship_base_firing_speed: int = field(init=False)
        ship_rapid_firing_speed: int = field(init=False)
        ship_base_fire_rate: int = 250
        ship_rapid_fire_rate: int = 175

        # Laser settings
        laser_graphic: Path = paths.Graphics.laser
        laser_noise: Path = paths.Audio.laser
        impact_noise: Path = paths.Audio.impact
        laser_size: Tuple[int, int] = field(init=False)
        laser_speed: int = field(init=False)

        # Alien settings
        alien_image: Path = paths.Graphics.alien
        alien_size: Tuple[int, int] = field(init=False)
        alien_value: int = 5

        # Horde settings
        horde_speed: int = field(init=False)
        horde_size: Tuple[int, int] = field(init=False)
        horde_advance: int = field(init=False)
        horde_direction: int = 1
        horde_padding: int = field(init=False)

        def __post_init__(self):
                """
                Compute dynamic values based on screen size and debugging mode.
                """
                self.screen_size = self.ScreenSize()

                # UI Labels
                self.hi_score_size = self.screen_size[1] // 25
                self.hi_score_loc = (
                        self.screen_size[0] - (self.screen_size[0] // 10),
                        self.screen_size[1] // 50
                )

                self.score_size = self.screen_size[1] // 25
                self.score_loc = (
                        self.screen_size[0] // 2,
                        self.screen_size[1] // 50
                )

                self.wave_size = self.screen_size[1] // 25
                self.wave_loc = (
                        self.screen_size[0] // 17,
                        self.screen_size[1] // 50
                )

                self.play_button_font_size = self.screen_size[0] // 35
                self.play_button_loc = (
                        (self.screen_size[0] - (self.screen_size[0] // 2)),
                        (self.screen_size[1] - (self.screen_size[1] // 2))
                )

                self.pause_button_font_size = self.screen_size[0] // 60
                self.pause_button_loc = (
                        self.screen_size[0] - (self.screen_size[0] // 25),
                        int(self.screen_size[1] * 0.07)
                )

                # Ship dimensions
                self.ship_size = (
                        self.screen_size[0] // 15,
                        self.screen_size[1] // 10
                )
                self.life_display_icon_size = (
                        self.ship_size[0] - (self.ship_size[0] // 3),
                        self.ship_size[1] - (self.ship_size[1] // 3)
                )
                self.life_display_padding = self.life_display_icon_size[0] + 6
                self.life_display_loc = (
                        self.screen_size[0] // 150,
                        self.screen_size[1] // 20
                )
                self.ship_speed = self.screen_size[0] // 150
                self.ship_base_firing_speed = self.ship_speed - (self.ship_speed // 3)
                self.ship_rapid_firing_speed = self.ship_speed // 2

                # Laser dimensions
                self.laser_size = (
                        self.screen_size[0] // 60,
                        self.screen_size[1] // 20
                )
                self.laser_speed = self.screen_size[0] // 125

                # Alien dimensions
                self.alien_size = (
                        self.screen_size[0] // 25,
                        self.screen_size[1] // 15
                )
                self.horde_advance = self.alien_size[1]

                # Horde settings
                if self.DEBUGGING:
                        self.horde_speed = self.screen_size[0] // 121
                        self.horde_size = (9, 14)
                else:
                        self.horde_speed = self.screen_size[0] // 365
                        self.horde_size = (6, 14)

                self.horde_padding = self.screen_size[0] // 147

        def ScreenSize(self) -> Tuple[int, int]:
                """
                Compute the usable screen area for the game window.

                Adjust for macOS menu bar if necessary.
                """
                pygame.display.init()

                if self.DEBUGGING:
                        x, y = 900, 450
                else:
                        x = pygame.display.get_desktop_sizes()[0][0]
                        y = pygame.display.get_desktop_sizes()[0][1]
                        if platform.system() == 'Darwin':
                                y -= 61  # approximate macOS menu bar height

                return (x, y)
