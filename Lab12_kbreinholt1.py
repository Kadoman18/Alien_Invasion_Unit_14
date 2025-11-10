import pygame
import sys
from types import SimpleNamespace # wanted dot operators, got this from ai.

# TODO update later for full screen (x=3000, y=1500)
screen_size = SimpleNamespace(x=900, y=450)

font_cache = {}
fonts = {
        'ss_reg': 'assets/fonts/Silkscreen/Silkscreen-Regular.ttf',
        'ss_bold': 'assets/fonts/Silkscreen/Silkscreen-Bold.ttf'
}

def get_font(font_key, size):
        if font_key not in font_cache:
                font_cache[font_key] = {}

        if size not in font_cache[font_key]:
                font_cache[font_key][size] = pygame.font.Font(fonts[font_key], size)

        return font_cache[font_key][size]

def wave() -> None:
        wave = 1
        return f'Wave: {wave}'

def text_label(text, font_key, size, color) -> None:
        font = get_font(font_key, size)
        return font.render(text, False, color)

def main():
        pygame.init()
        screen = pygame.display.set_mode((screen_size.x, screen_size.y))
        pygame.display.set_caption("👾 Alien Invasion 👾")
        clock = pygame.time.Clock()

        sky_surf = pygame.image.load('assets/graphics/Starbasesnow.png').convert()

        ship_surf = pygame.image.load('assets/graphics/ship.png').convert_alpha()
        ship_rect = ship_surf.get_rect(midbottom=(450, 440))

        laser_blast_surface = pygame.image.load('assets/graphics/laserBlast.png').convert_alpha()
        enemy_surface = pygame.image.load('assets/graphics/enemy_4.png').convert_alpha()

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                screen.blit(sky_surf, (0, 0))
                screen.blit(text_label(wave(), 'ss_reg', 25, "White"), (10, 10))

                ship_rect.x += 4

                if ship_rect.right <= 0: ship_rect.left = screen_size.x
                if ship_rect.left >= screen_size.x: ship_rect.right = 0

		# TODO
                # if laser_blast_rect.colliderect(enemy_rect)
			# CODE IT


                screen.blit(ship_surf, ship_rect)

                pygame.display.update()
                clock.tick(60)

if __name__ == '__main__':
        main()
