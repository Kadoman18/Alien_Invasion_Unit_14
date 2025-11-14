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
        impact: Path = BASE / "audio" / "impactSound.mp3"
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
                Path to the bold-weight Silkscreen font.
        regular : Path
                Path to the regular-weight Silkscreen font.
        """
        bold: Path = BASE / "fonts" / "Silkscreen-Bold.ttf"
        regular: Path = BASE / "fonts" / "Silkscreen-Regular.ttf"


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
                Beam/laser graphic asset.
        enemy : Path
                Enemy ship sprite.
        laser : Path
                Laser blast sprite.
        ship1 : Path
                Primary player ship sprite.
        ship2 : Path
                Alternate player ship sprite.
        ship2nobg : Path
                Ship sprite with background removed.
        background : Path
                Primary game background image.
        """
        asteroid: Path = BASE / "graphics" / "Asteroid Brown.png"
        beams: Path = BASE / "graphics" / "beams.png"
        enemy: Path = BASE / "graphics" / "enemy_4.png"
        laser: Path = BASE / "graphics" / "laserBlast.png"
        ship1: Path = BASE / "graphics" / "ship.png"
        ship2: Path = BASE / "graphics" / "ship2.png"
        ship2nobg: Path = BASE / "graphics" / "ship2(no bg).png"
        background: Path = BASE / "graphics" / "Starbasesnow.png"
