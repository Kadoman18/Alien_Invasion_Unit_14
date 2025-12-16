"""
Module providing the main Alien Invasion game loop using pygame.

Includes the core game window initialization, event handling, and game state management.
"""

import alien_horde
import game_stats
import hud
import ship
import pygame
import settings
from dataclasses import dataclass


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

        # Initialize local variables
        def __init__(self) -> None:

                # Initialize pygame
                pygame.init()

                # Reference settings
                self.settings = settings.Settings()

                # Reference stats
                self.stats = game_stats.GameStats(self)

                # Set the screen mode, scaling depending on screen size
                self.screen = pygame.display.set_mode((self.settings.screen_size))

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
                        background=pygame.transform.scale(pygame.image.load(self.settings.background).convert(), self.settings.screen_size),
                        icon=pygame.image.load(self.settings.icon)
                )

                # Reference HUD
                self.hud = hud.HUD(self)

                # Define the screen rect for sprite placements
                self.screen_rect: pygame.Rect = self.screen.get_rect(
                        midbottom=(
                                self.settings.screen_size[0] // 2,
                                self.settings.screen_size[1]
                        )
                )

                # Initialize pause timer
                self.pause_duration = 0
                self.pause_start_time = None

                # Customize game window title and icon
                pygame.display.set_caption(self.settings.name)
                pygame.display.set_icon(self.resources.icon)

                # Load and resize the sky image to fit the window and get its rect
                self.sky_image: pygame.Surface = self.resources.background
                self.sky_rect: pygame.Rect = self.sky_image.get_rect()

                # Create the player's ship sprite, sprite group, and add the sprite to it.
                self.ship = ship.Ship(self, self.resources)
                self.ship_group = pygame.sprite.GroupSingle()
                self.ship_group.add(self.ship)

                # Create the lasers sprite group
                self.lasers = pygame.sprite.Group()

                # Create the horde of aliens
                self.horde = alien_horde.AlienHorde(self, self.resources)

                # Player hasnt lost.. yet..
                self.you_lose: bool = False

                # Game running boolean
                self.running: bool = True

                # Game paused boolean
                self.paused: bool = True

                # Game clock
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
                        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                                        if (self.hud.play_button.rect.collidepoint(pygame.mouse.get_pos())
                                             or self.hud.pause_button.rect.collidepoint(pygame.mouse.get_pos())):
                                                self._toggle_pause()

                        # Keydown event
                        elif event.type == pygame.KEYDOWN:
                                self._key_down_event(event)

                        # Keyup event
                        elif event.type == pygame.KEYUP:
                                self._key_up_event(event)


        def _key_down_event(self, event) -> None:
                """Listens for key down events (Key Presses)"""

                # Rightward movement
                if event.key == pygame.K_d and not self.you_lose:
                        self.ship.state.moving_right = True
                elif event.key == pygame.K_RIGHT and not self.you_lose:
                        self.ship.state.moving_right = True

                # Leftward movement
                elif event.key == pygame.K_a and not self.you_lose:
                        self.ship.state.moving_left = True
                elif event.key == pygame.K_LEFT and not self.you_lose:
                        self.ship.state.moving_left = True

                # Firing (base and rapid)
                elif event.key == pygame.K_SPACE:
                        self.ship.state.firing = True
                elif event.key == pygame.K_LSHIFT:
                        self.ship.state.firing_rapid = True

                # Quit game with Escape
                elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.quit()
                        exit()


        def _key_up_event(self, event) -> None:
                """Listens for key up events (Key Releases)"""

                # Pause button
                if event.key == pygame.K_p:
                        self._toggle_pause()

                # Rightward movement stop
                elif event.key == pygame.K_d or self.you_lose:
                        self.ship.state.moving_right = False
                elif event.key == pygame.K_LEFT or self.you_lose:
                        self.ship.state.moving_left = False

                # Leftward movement stop
                elif event.key == pygame.K_a or self.you_lose:
                        self.ship.state.moving_left = False
                elif event.key == pygame.K_RIGHT or self.you_lose:
                        self.ship.state.moving_right = False

                # Firing stop
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


        def on_descent_complete(self) -> None:
                self.you_lose = False

                self.stats.lives_left -= 1

                if self.stats.lives_left > 0:
                        self.ship_group.empty()
                        self.ship = ship.Ship(self, self.resources)
                        self.ship_group.add(self.ship)

                        self.horde.reset()

                        self.paused = False
                else:
                        self.running = False


        def _update_screen(self) -> None:
                """Updates the screen with relevant movements, sprites, and UI elements"""

                # Draw background
                self.screen.blit(self.sky_image, (0, 0))

                # Draw ship sprite
                self.ship_group.draw(self.screen)

                # Draw lasers sprite group
                self.lasers.draw(self.screen)

                # Draw alien horde
                self.horde.group.draw(self.screen)

                # Draw HUD
                self.hud.draw(self.screen)

                # Update the display (swap buffers)
                pygame.display.flip()


        def run_game(self) -> None:
                """Main game loop"""

                while self.running:
                        self._event_listener()

                        if not self.paused:
                                self.ship_group.update()
                                self.lasers.update()
                                self.horde.update()

                        self._update_screen()
                        self.clock.tick(self.settings.fps)


if __name__ == '__main__':
        AlienInvasion().run_game()
