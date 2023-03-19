import pygame, sys
from settings import *
from units import *
from pytmx.util_pygame import load_pygame
from debug import *
class AllSprites(pygame.sprite.Group):
    def __init__(self, map_width, map_height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

        self.ground_surf = pygame.image.load('data/bg.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        self.keyboard_speed = 500

        self.map_width = map_width
        self.map_height = map_height

        self.selecting = False

    def keyboard_control(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.offset.x >= 0: self.offset.x -= self.keyboard_speed * dt
        if keys[pygame.K_RIGHT] and self.offset.x <= self.map_width - WINDOW_WIDTH: self.offset.x += self.keyboard_speed * dt
        if keys[pygame.K_UP] and self.offset.y >= 0: self.offset.y -= self.keyboard_speed * dt
        if keys[pygame.K_DOWN] and self.offset.y <= self.map_height - WINDOW_HEIGHT: self.offset.y += self.keyboard_speed * dt

    def draw_selection(self):
        mouse = pygame.mouse.get_pressed()

        if mouse[0] and not self.selecting:
            self.start_pos_x = pygame.mouse.get_pos()[0] + self.offset.x
            self.start_pos_y = pygame.mouse.get_pos()[1] + self.offset.y
            self.selecting = True
        elif not mouse[0] and self.selecting:
            self.selecting = False

        if self.selecting:
            self.end_pos_x = pygame.mouse.get_pos()[0] + self.offset.x
            self.end_pos_y = pygame.mouse.get_pos()[1] + self.offset.y
            selection_rect = pygame.Rect((min(self.start_pos_x, self.end_pos_x), min(self.start_pos_y, self.end_pos_y)),
                                         (abs(self.end_pos_x - self.start_pos_x), abs(self.end_pos_y - self.start_pos_y)))
            self.image = pygame.Surface((selection_rect.width, selection_rect.height))
            self.image.set_alpha(80)
            self.display_surface.blit(self.image, selection_rect.topleft - self.offset)
        else:
            self.image = pygame.Surface((0, 0))

    def custom_draw(self, dt):
        self.keyboard_control(dt)

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        self.draw_selection()

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('vikingz')
        self.clock = pygame.time.Clock()

        self.tmx_map = load_pygame('data/map.tmx')
        map_width = self.tmx_map.width * self.tmx_map.tilewidth
        map_height = self.tmx_map.height * self.tmx_map.tileheight

        self.all_sprites = AllSprites(map_width, map_height)
        self.units = pygame.sprite.Group()

        self.setup()

    def setup(self):

        for obj in self.tmx_map.get_layer_by_name('Entities'):
            if obj.name == "Warrior1":
                Warrior1((obj.x, obj.y), [self.all_sprites, self.units], PATHS['warrior1'])
            if obj.name == "Warrior2":
                Warrior2((obj.x, obj.y), [self.all_sprites, self.units], PATHS['warrior2'])
            if obj.name == "Warrior3":
                Warrior3((obj.x, obj.y), [self.all_sprites, self.units], PATHS['warrior3'])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.display_surface.fill('black')

            self.all_sprites.update(dt)
            self.all_sprites.custom_draw(dt)

            # print(int(self.clock.get_fps()))
            # print(len(self.all_sprites))

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()