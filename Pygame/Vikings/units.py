import pygame
from pygame.math import Vector2 as vector
from settings import *
from pathlib import Path

class Unit(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path):
        super().__init__(groups)

        self.import_assets(path)
        self.frame_index = 0
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height / 2)
        self.health = 100
        self.max_health = 200

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount

    def get_health(self, amount):
        if self.health < self.max_health:
            self.health += amount

    def import_assets(self, path):
        root_dir = Path(path)
        self.animations = {}
        for path in root_dir.iterdir():
            self.animations[str(path).split('\\')[-1]] = \
                [pygame.image.load(file).convert_alpha() for file in Path(path).iterdir() if file.is_file()]

class Warrior1(Unit):
    def __init__(self, pos, groups, path):
        super().__init__(pos, groups, path)
        self.selected = False
        self.health = 100
        self.max_health = 200

        self.display_surf = pygame.display.get_surface()

    def basic_health(self):
        if self.selected:
            pygame.draw.rect(self.display_surf, (255, 0, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width, 10))
            pygame.draw.rect(self.display_surf, (0, 255, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width * (self.health / self.max_health), 10))

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def check_selection(self):
        if self.selection.colliderect(self.rect):
            print('warrior selected')
            self.selected = True
        else:
            self.selected = False

    def update(self, dt):
        self.animate(dt)
        # self.check_selection()
        self.basic_health()
        self.get_damage(0.05)
        self.rect.x += 1

class Warrior2(Unit):
    def __init__(self, pos, groups, path):
        super().__init__(pos, groups, path)
        # self.selection = selection_rect
        self.selected = False
        self.health = 100
        self.max_health = 200

        self.display_surf = pygame.display.get_surface()

    def basic_health(self):
        if self.selected:
            pygame.draw.rect(self.display_surf, (255, 0, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width, 10))
            pygame.draw.rect(self.display_surf, (0, 255, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width * (self.health / self.max_health), 10))

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    # def check_selection(self):
    #     for selection in self.selection.sprites():
    #         if selection.rect.colliderect(self.rect):
    #             self.selected = True
    #         else:
    #             self.selected = False

    def update(self, dt):
        self.basic_health()
        self.animate(dt)
        # self.check_selection()
        self.get_damage(0.05)

class Warrior3(Unit):
    def __init__(self, pos, groups, path):
        super().__init__(pos, groups, path)
        # self.selection = selection_rect
        self.selected = False
        self.health = 100
        self.max_health = 200

        self.display_surf = pygame.display.get_surface()

    def basic_health(self):
        if self.selected:
            pygame.draw.rect(self.display_surf, (255, 0, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width, 10))
            pygame.draw.rect(self.display_surf, (0, 255, 0), (self.rect.left, self.rect.top + 10,
                                                              self.rect.width * (self.health / self.max_health), 10))

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    # def check_selection(self):
    #     for selection in self.selection.sprites():
    #         if selection.rect.colliderect(self.rect):
    #             self.selected = True
    #         else:
    #             self.selected = False

    def update(self, dt):
        self.basic_health()
        self.animate(dt)
        # self.check_selection()
        self.get_damage(0.05)