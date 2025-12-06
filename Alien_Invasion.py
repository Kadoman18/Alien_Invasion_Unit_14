"""
Module providing the main Alien Invasion game loop using pygame.
Includes the core game window initialization.
"""

import pygame
import settings
from ship import Ship
from alien_horde import AlienHorde
from button import Button


class AlienInvasion:
        """Main game controller for the Alien Invasion application."""

        def __init__(self) -> None:

                # Initialize
                pygame.init()
                self.settings = settings.Settings()

                # Set the screen mode, scaling depending on screen size
                self.screen = pygame.display.set_mode((self.settings.screen_size))

                # Define the screen rect for sprite placements
                self.screen_rect: pygame.Rect = self.screen.get_rect(
                        midbottom=(
                                self.settings.ScreenSize.x // 2,
                                self.settings.ScreenSize.y
                        )
                )

                # Initialize pause timer
                self.pause_duration = 0
                self.pause_start_time = None

                self.play_button = Button(
                        self.settings.play_button_text,
                        self.settings.play_button_font,
                        self.screen_rect.center,
                        self.settings.screen_size[0] // 35,
                        "white",
                        "green",
                        self
                        )
                self.play_button_rect = self.play_button.rect

                # Customize game window title and icon
                pygame.display.set_caption(self.settings.name)
                pygame.display.set_icon(pygame.image.load(self.settings.icon))

                # Load and resize the sky image to fit the window and get its rect
                self.sky_image: pygame.Surface = pygame.transform.scale(
                        pygame.image.load(self.settings.background).convert(),
                        self.settings.screen_size
                )
                self.sky_rect: pygame.Rect = self.sky_image.get_rect()

                # Create the player's ship sprite, sprite group, and add the sprite to it.
                self.ship = Ship(self)
                self.ship_group = pygame.sprite.GroupSingle()
                self.ship_group.add(self.ship)

                # Create the lasers sprite group
                self.lasers = pygame.sprite.Group()
                self.lasers_noise = pygame.mixer.Sound(self.settings.laser_noise)

                # Create the horde of aliens
                self.horde = AlienHorde(self)

                # Game running boolean
                self.running: bool = True

                # Game paused boolean
                self.paused: bool = True

                # Game clock
                self.clock = pygame.time.Clock()



        def _event_listener(self) -> None:
                """Listens for events like quit, or keyboard input."""

                for event in pygame.event.get():
                        # Quit game
                        if event.type == pygame.QUIT:
                                self.running = False
                                pygame.quit()
                                exit()

                        # Mouse Right Click event
                        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                                        if self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
                                                self._toggle_pause()

                        # Keydown event
                        elif event.type == pygame.KEYDOWN:
                                self._key_down_event(event)

                        # Keyup event
                        elif event.type == pygame.KEYUP:
                                self._key_up_event(event)


        def _key_down_event(self, event):
                """Listens for key down events (Key Presses)"""

                # Rightward movement
                if event.key == pygame.K_d:
                        self.ship.moving_right = True
                elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True

                # Leftward movement
                elif event.key == pygame.K_a:
                        self.ship.moving_left = True
                elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = True

                # Firing (base and rapid)
                elif event.key == pygame.K_SPACE:
                        self.ship.firing = True
                elif event.key == pygame.K_LSHIFT:
                        self.ship.firing_rapid = True

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
                elif event.key == pygame.K_d:
                        self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = False

                # Leftward movement stop
                elif event.key == pygame.K_a:
                        self.ship.moving_left = False
                elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False

                # Firing stop
                elif event.key == pygame.K_SPACE:
                        self.ship.firing = False
                elif event.key == pygame.K_LSHIFT:
                        self.ship.firing_rapid = False

        def _toggle_pause(self) -> None:
                """
                Handles the play button rect and the effects on the laser
                fire cooldown of the game pausing
                """
                if not self.paused:

                        # Going from unpaused to paused
                        self.paused = True

                        self.play_button.rect.center = self.screen_rect.center

                        # Get current tick for pause start time
                        self.pause_start_time = pygame.time.get_ticks()
                else:

                        # Going from paused to unpaused
                        self.paused = False
                        paused_time = 0

                        self.play_button.rect.center = (-10000, -10000)

                        # Calculate pause duration
                        if self.pause_start_time != None:
                                paused_time = pygame.time.get_ticks() - self.pause_start_time
                        self.pause_duration += paused_time

                        # Set pause timer to None
                        self.pause_start_time = None

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

                # Draw play button when paused
                if self.paused:
                        self.play_button.draw(self.screen)

                # Update the display (swap buffers)
                pygame.display.flip()


        def run_game(self) -> None:
                """Main game loop"""
                while self.running == True:
                        # Handle system and player events
                        self._event_listener()

                        # Update ship sprite group
                        self.ship_group.update()

                        # Update lasers sprite group
                        self.lasers.update()

                        # Update alien horde movement
                        self.horde.update()

                        # Draws all relevant surfaces, rects, sprites, to the screen.
                        self._update_screen()

                        # Limit framerate to avoid running too fast
                        self.clock.tick(self.settings.fps)


if __name__ == '__main__':
        AlienInvasion().run_game()
