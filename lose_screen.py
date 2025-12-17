"""
Lose screen overlay for Alien Invasion.

Uses the existing Panel UI system for buttons and TextLabel for text.
"""

import pygame
from typing import TYPE_CHECKING
from pathlib import Path
from hud import Panel, PanelData, TextLabel, LabelData

if TYPE_CHECKING:
        from Alien_Invasion import AlienInvasion


class LoseScreen:
        """Handles rendering and interaction for the lose screen."""

        def __init__(self, game: 'AlienInvasion') -> None:
                self.game = game
                self.screen = game.screen
                self.settings = game.settings
                self.stats = game.stats
                self.screen_rect = self.screen.get_rect()

                # ---------- Text labels ----------
                title_size = int(self.settings.screen_size[1] // 7.5)
                score_size = int(self.settings.screen_size[1] // 17.5)

                title_font = Path(self.settings.fonts['ss_bold'])
                score_font = Path(self.settings.fonts['ss_reg'])

                self.title_label = TextLabel(
                        game,
                        LabelData(
                                text="YOU LOST",
                                text_size=title_size,
                                center=(self.screen_rect.centerx, self.screen_rect.centery - 120),
                                color="red"
                        ),
                        title_font
                )

                self.score_label = TextLabel(
                        game,
                        LabelData(
                                text=f"Score: {self.stats.score}",
                                text_size=score_size,
                                center=(self.screen_rect.centerx, self.screen_rect.centery - 40),
                                color="white"
                        ),
                        score_font
                )

                # ---------- Panel buttons ----------
                button_font = Path(self.settings.fonts['ss_reg'])
                button_size = int(self.settings.screen_size[1] // 12.5)

                play_again_data = PanelData(
                        text="Play Again",
                        center=(self.screen_rect.centerx, int(self.screen_rect.bottom * 0.6)),
                        text_size=button_size,
                        text_color="white",
                        fill_color="purple",
                        border_color="gray"
                )

                quit_data = PanelData(
                        text="Quit",
                        center=(self.screen_rect.centerx, int(self.screen_rect.bottom * 0.85)),
                        text_size=button_size,
                        text_color="white",
                        fill_color="red",
                        border_color="gray"
                )

                self.play_again_button = Panel(game, play_again_data, button_font)
                self.quit_button = Panel(game, quit_data, button_font)


        def draw(self) -> None:
                """Draws the lose screen."""
                self.screen.fill("black")

                # Update the score label text to the final score
                self.score_label.set_text(f"Score: {self.stats.score}")

                # Draw text labels
                self.screen.blit(self.title_label.surface, self.title_label.rect)
                self.screen.blit(self.score_label.surface, self.score_label.rect)

                # Draw buttons with label
                for button in [self.play_again_button, self.quit_button]:
                        # Fill panel surface with fill color and draw border
                        button.surface.fill(button.data.border_color)
                        inner_rect = button.surface.get_rect()
                        inner_rect.inflate_ip(-button.padding[0], -button.padding[1])
                        inner_rect.center = button.surface.get_rect().center
                        button.surface.fill(button.data.fill_color, inner_rect)

                        # Draw label centered on panel
                        label_rect = button.label.surface.get_rect(center=button.surface.get_rect().center)
                        button.surface.blit(button.label.surface, label_rect)

                        # Blit panel to screen
                        self.screen.blit(button.surface, button.rect)




        def handle_click(self, mouse_pos: tuple[int, int]) -> None:
                """Handles mouse interaction."""
                if self.play_again_button.rect.collidepoint(mouse_pos):
                        self.game.restart_game()
                elif self.quit_button.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
