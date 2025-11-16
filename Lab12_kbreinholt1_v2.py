"""
Module providing the main Alien Invasion game loop using pygame.
Includes the core game window initialization.
"""

import pygame
from settings import Settings
from ship import Ship
from laser import Laser

class AlienInvasion:
        """
        Main game controller for the Alien Invasion application.

        Handles:
        - pygame initialization
        - window configuration
        - background loading and scaling
        - ship creation
        - main game loop execution
        """

        def __init__(self):
                """
                Initialize game settings, window, background, and runtime systems.
                """

                # Prepare all pygame subsystems
                pygame.init()

                # Load configuration settings (screen size, paths, FPS, etc.)
                self.settings = Settings()

                # Create main game window with configured resolution
                self.screen = pygame.display.set_mode((self.settings.screen_size))

                # Screen rectangle used for positioning objects consistently
                self.screen_rect = self.screen.get_rect(
                        midbottom=(
                                self.settings.ScreenSize.x // 2,
                                self.settings.ScreenSize.y
                        )
                )

                # Window title and icon loaded from settings
                pygame.display.set_caption(self.settings.name)
                pygame.display.set_icon(pygame.image.load(self.settings.icon))

                # Load and scale background to fill entire window
                self.sky_surf = pygame.transform.scale(
                        pygame.image.load(self.settings.background).convert(),
                        self.settings.screen_size
                )
                self.sky_rect = self.sky_surf.get_rect()

                # Create the player's ship, passing this game instance for access
                self.ship = Ship(self)

                # Create the laser
                self.laser = Laser(self)

                # Runtime flags
                self.running = True

                # Clock object used to regulate FPS
                self.clock = pygame.time.Clock()


        def _event_listener(self):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                self.running = False
                                pygame.quit()
                                exit()
                        elif event.type == pygame.KEYDOWN:
                                self._key_down_event(event)
                        elif event.type == pygame.KEYUP:
                                self._key_up_event(event)


        def _key_down_event(self, event):
                if event.key == pygame.K_a:
                        self.ship.moving_left = True
                elif event.key == pygame.K_d:
                        self.ship.moving_right = True
                elif event.key == pygame.K_SPACE:
                        self.laser.draw()
                        self.ship.firing = True
                elif event.key == pygame.K_q:
                        self.running = False
                        pygame.quit()
                        exit()


        def _key_up_event(self, event):
                if event.key == pygame.K_a:
                        self.ship.moving_left = False
                elif event.key == pygame.K_d:
                        self.ship.moving_right = False
                elif event.key == pygame.K_SPACE:
                        self.ship.firing = False


        def _update_screen(self):
                # Draw background to window
                self.screen.blit(self.sky_surf, (0, 0))

                # Draw player ship
                self.ship.draw()

                # Update the display (swap buffers)
                pygame.display.flip()


        def run_game(self) -> None:
                """
                Execute the main game loop until the window is closed.
                """

                self.ship_sprite = pygame.sprite.GroupSingle().add(Ship(self))

                self.laser_sprite = pygame.sprite.Group().add(Laser(self))

                while self.running:

                        # Handle system and player events (closing window, etc.)
                        self._event_listener()

                        # Updates the ships current position with inputs
                        self.ship.update()

                        self.laser.update()

                        # Draws all relevant surfaces, rects, sprites, to the screen.
                        self._update_screen()

                        # Limit framerate to avoid running too fast
                        self.clock.tick(self.settings.fps)



if __name__ == '__main__':
        AlienInvasion().run_game()
