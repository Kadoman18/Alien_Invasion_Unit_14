"""
Asset path definitions for the Alien Invasion game.

Provides typed dataclasses exposing file paths for audio, JSON data,
fonts, and graphics assets. All paths resolve relative to the project’s
./assets directory at runtime.
"""

from pathlib import Path
from dataclasses import dataclass


BASE = Path.cwd() / 'assets'


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
        impact: Path = BASE / "audio" / "impact.mp3"
        laser: Path = BASE / "audio" / "laser.mp3"


@dataclass
class File:
        """
        File paths for data and JSON-based persistent storage.

        Attributes
        ----------
        scores : Path
                Path to the JSON file storing player score data.
        """
        scores: Path = BASE / "file" / "scores.json"


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
        bold: Path = BASE / "fonts" / "silkscreen" / "silkscreen_bold.ttf"
        regular: Path = BASE / "fonts" / "silkscreen" / "silkscreen_regular.ttf"


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
        asteroid: Path = BASE / "graphics" / "asteroid.png"
        beams: Path = BASE / "graphics" / "beams.png"
        alien: Path = BASE / "graphics" / "alien.png"
        laser: Path = BASE / "graphics" / "laser.png"
        ship: Path = BASE / "graphics" / "ship.png"
        background: Path = BASE / "graphics" / "background.png"
        icon: Path = BASE / "graphics" / "icon.png"
