"""
Module providing the main Alien Invasion game loop using pygame.
Includes the core game window initialization.
"""

import pygame
from settings import Settings
from ship import Ship
from arsenal import Laser
from alien_ships import Aliens


class AlienInvasion:
        """Main game controller for the Alien Invasion application."""

        def __init__(self) -> None:

                # Initialize
                pygame.init()
                self.settings = Settings()

                # Set the screen mode, scaling depending on screen size
                self.screen = pygame.display.set_mode((self.settings.screen_size))

                # Define the screen rect for sprite placements
                self.screen_rect: pygame.Rect = self.screen.get_rect(
                        midbottom=(
                                self.settings.ScreenSize.x // 2,
                                self.settings.ScreenSize.y
                        )
                )

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

                self.laser_blast = pygame.mixer.music.load(self.settings.laser_noise)

                # Alien Sprite
                self.alien = Aliens(self)
                self.aliens = pygame.sprite.Group()

                # Game running boolean
                self.running: bool = True

                # Game clock
                self.clock = pygame.time.Clock()


        def _fire_laser(self) -> None:
                """Handles the logic for continuous laser firing and rate"""

                # Get current time for fire rate limiting
                now: int = pygame.time.get_ticks()

                # Give laser the last shot time attribute
                if not hasattr(self, "last_shot_time"):
                        self.last_shot_time = 0

                # Base fire speed (spacebar)
                if self.ship.firing and (now - self.last_shot_time >= self.settings.ship_base_fire_rate):
                        laser = Laser(self)
                        self.lasers.add(laser)
                        pygame.mixer.music.play()
                        self.last_shot_time = now

                # Rapid fire speed (spacebar + shift)
                elif self.ship.firing and self.ship.firing_rapid and (now - self.last_shot_time >= self.settings.ship_rapid_fire_rate):
                        laser = Laser(self)
                        self.lasers.add(laser)
                        pygame.mixer.music.play()
                        self.last_shot_time = now


        def _event_listener(self) -> None:
                """Listens for events like quit, or keyboard input."""

                for event in pygame.event.get():
                        # Quit game
                        if event.type == pygame.QUIT:
                                self.running = False
                                pygame.quit()
                                exit()

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

                # Rightward movement stop
                if event.key == pygame.K_d:
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


        def _update_screen(self) -> None:
                """Updates the screen with relevant movements, sprites, and UI elements"""

                # Draw background
                self.screen.blit(self.sky_image, (0, 0))

                # Draw ship sprite
                self.ship_group.draw(self.screen)

                # Draw lasers sprite group
                self.lasers.draw(self.screen)

                # Draw aliens sprite group
                self.aliens.draw(self.screen)

                # Update the display (swap buffers)
                pygame.display.flip()


        def run_game(self) -> None:
                """Main game loop"""

                self.aliens.add(self.alien)

                while True:

                        # Handle system and player events
                        self._event_listener()

                        # Update ship sprite group
                        self.ship_group.update()

                        # Fire lasers if conditions are met
                        self._fire_laser()

                        # Update lasers sprite group
                        self.lasers.update()

                        # Draws all relevant surfaces, rects, sprites, to the screen.
                        self._update_screen()

                        # Limit framerate to avoid running too fast
                        self.clock.tick(self.settings.fps)


if __name__ == '__main__':
        AlienInvasion().run_game()
