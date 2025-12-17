"""
Module providing the main Alien Invasion game loop using pygame.

Includes the core game window initialization, event handling, and game state management.
"""

import alien_horde
import game_stats
import hud
import lose_screen
import ship
import pygame
import settings
from dataclasses import dataclass
from enum import Enum, auto


class GameState(Enum):
        SPAWNING = auto()
        PLAYING = auto()
        DESCENT = auto()
        LOSE_DELAY = auto()
        LOSE_SCREEN = auto()


@dataclass
class Resources:
        """Dataclass to cache preloaded images and sounds for smoother gameplay"""
        ship_image: pygame.Surface
        laser_image: pygame.Surface
        alien_image: pygame.Surface
        laser_sound: pygame.mixer.Sound
        impact_sound: pygame.mixer.Sound
        background: pygame.Surface
        icon: pygame.Surface


class AlienInvasion:
        """Main game controller for the Alien Invasion application."""

        def __init__(self) -> None:
                pygame.init()

                self.settings = settings.Settings()
                self.stats = game_stats.GameStats(self)

                self.screen = pygame.display.set_mode((self.settings.screen_size))

                # Player input lock (disabled during horde spawn)
                self.allow_player_input: bool = False

                # Preload resources
                self.resources = Resources(
                        ship_image=pygame.image.load(self.settings.ship_image).convert_alpha(),
                        laser_image=pygame.image.load(self.settings.laser_graphic).convert_alpha(),
                        alien_image=pygame.transform.scale(
                                pygame.image.load(self.settings.alien_image).convert_alpha(),
                                self.settings.alien_size
                        ),
                        laser_sound=pygame.mixer.Sound(self.settings.laser_noise),
                        impact_sound=pygame.mixer.Sound(self.settings.impact_noise),
                        background=pygame.transform.scale(
                                pygame.image.load(self.settings.background).convert(),
                                self.settings.screen_size
                        ),
                        icon=pygame.image.load(self.settings.icon)
                )

                self.hud = hud.HUD(self)

                self.screen_rect = self.screen.get_rect(
                        midbottom=(
                                self.settings.screen_size[0] // 2,
                                self.settings.screen_size[1]
                        )
                )

                pygame.display.set_caption(self.settings.name)
                pygame.display.set_icon(self.resources.icon)

                self.sky_image = self.resources.background
                self.sky_rect = self.sky_image.get_rect()

                self.ship = ship.Ship(self, self.resources)
                self.ship_group = pygame.sprite.GroupSingle()
                self.ship_group.add(self.ship)

                self.lasers = pygame.sprite.Group()

                # Create alien horde (starts in spawning state)
                self.horde = alien_horde.AlienHorde(self, self.resources)

                self.you_lose: bool = False
                self.running: bool = True
                self.paused: bool = True

                # Pause timing
                self.pause_start_time: int | None = None
                self.pause_duration: int = 0

                # Set initial state
                self.state: GameState = GameState.SPAWNING

                # Lose screen
                self.lose_screen = lose_screen.LoseScreen(self)

                # Lose screen timing
                self.lose_time_start: int | None = None
                self.lose_delay_ms: int = 1000

                self.clock = pygame.time.Clock()


        def _event_listener(self) -> None:
                """Listens for events like quit, or keyboard input."""

                # Get all events
                for event in pygame.event.get():

                        # Quit game
                        if event.type == pygame.QUIT:
                                self.running = False
                                pygame.quit()
                                exit()

                        # Mouse left click event
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                                if self.state == GameState.LOSE_SCREEN:
                                        self.lose_screen.handle_click(event.pos)
                                        return

                                if (self.hud.play_button.rect.collidepoint(event.pos)
                                or self.hud.pause_button.rect.collidepoint(event.pos)):
                                        self._toggle_pause()

                        # Keydown event
                        elif event.type == pygame.KEYDOWN:
                                self._key_down_event(event)

                        # Keyup event
                        elif event.type == pygame.KEYUP:
                                self._key_up_event(event)


        def _key_down_event(self, event) -> None:
                """Listens for key down events (Key Presses)"""

                # Ignore gameplay input during spawn or pause
                if not self.allow_player_input or self.paused:
                        return

                if event.key in (pygame.K_d, pygame.K_RIGHT) and not self.you_lose:
                        self.ship.state.moving_right = True

                elif event.key in (pygame.K_a, pygame.K_LEFT) and not self.you_lose:
                        self.ship.state.moving_left = True

                elif event.key == pygame.K_SPACE:
                        self.ship.state.firing = True

                elif event.key == pygame.K_LSHIFT:
                        self.ship.state.firing_rapid = True

                elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        exit()


        def _key_up_event(self, event) -> None:
                """Listens for key up events (Key Releases)"""

                # Pause always allowed
                if event.key == pygame.K_p:
                        self._toggle_pause()
                        return

                if not self.allow_player_input:
                        return

                if event.key in (pygame.K_d, pygame.K_RIGHT):
                        self.ship.state.moving_right = False

                elif event.key in (pygame.K_a, pygame.K_LEFT):
                        self.ship.state.moving_left = False

                elif event.key == pygame.K_SPACE:
                        self.ship.state.firing = False

                elif event.key == pygame.K_LSHIFT:
                        self.ship.state.firing_rapid = False



        def _toggle_pause(self) -> None:
                """
                Handles the play button rect and the effects on the laser
                fire cooldown of the game pausing
                """

                # Going from unpaused to paused
                if not self.paused:

                        # Pause game
                        self.paused = True

                        # Display the play button
                        self.hud.play_button.rect.center = self.screen_rect.center

                        # Get current tick for pause start time
                        self.pause_start_time = pygame.time.get_ticks()

                # Going from paused to unpaused
                else:

                        # Unpause game and reset pause timer
                        self.paused = False
                        paused_time = 0

                        # Calculate pause duration
                        if self.pause_start_time != None:
                                paused_time = pygame.time.get_ticks() - self.pause_start_time
                        self.pause_duration += paused_time

                        # Set pause timer to None
                        self.pause_start_time = None


        def on_horde_spawn_complete(self) -> None:
                """
                Called by AlienHorde when spawn descent finishes.
                Enables player input and begins active gameplay.
                """
                pygame.time.delay(500)
                self.allow_player_input = True
                self.state = GameState.PLAYING



        def on_descent_complete(self) -> None:
                self.you_lose = False
                self.stats.lives_left -= 1

                if self.stats.lives_left > 0:
                        self.ship_group.empty()
                        self.ship = ship.Ship(self, self.resources)
                        self.ship_group.add(self.ship)

                        self.allow_player_input = False
                        self.horde.reset()
                        self.paused = False
                else:
                        self.you_lose = True
                        self.state = GameState.LOSE_DELAY
                        self.lose_time_start = pygame.time.get_ticks()



        def _update_screen(self) -> None:
                """Updates the screen with relevant movements, sprites, and UI elements"""
                if self.state == GameState.LOSE_SCREEN:
                        self.lose_screen.draw()
                        pygame.display.flip()
                        return

                self.screen.blit(self.sky_image, (0, 0))
                self.ship_group.draw(self.screen)
                self.lasers.draw(self.screen)
                self.horde.group.draw(self.screen)
                self.hud.draw(self.screen)

                pygame.display.flip()


        def restart_game(self) -> None:
                self.stats.reset_stats()
                self.lasers.empty()
                self.ship_group.empty()

                self.ship = ship.Ship(self, self.resources)
                self.ship_group.add(self.ship)

                self.allow_player_input = False
                self.you_lose = False
                self.paused = False
                self.state = GameState.SPAWNING

                self.horde.reset()



        def run_game(self) -> None:
                while self.running:
                        self._event_listener()

                        if self.state == GameState.LOSE_DELAY:
                                now = pygame.time.get_ticks()
                                if self.lose_time_start != None and now - self.lose_time_start >= self.lose_delay_ms:
                                        self.state = GameState.LOSE_SCREEN

                        elif not self.paused and self.state != GameState.LOSE_SCREEN:
                                self.horde.update()

                                if self.state == GameState.PLAYING:
                                        self.ship_group.update()
                                        self.lasers.update()

                        self._update_screen()
                        self.clock.tick(self.settings.fps)


if __name__ == '__main__':
        AlienInvasion().run_game()
