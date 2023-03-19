import pygame
from pygame.math import Vector2 as vector
from settings import *
from pathlib import Path
from debug import debug

class Unit(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, selection):
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
        self.selected = False
        self.selection = selection

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount

    def get_health(self, amount):
        if self.health < self.max_health:
            self.health += amount

    def basic_health(self):
        if self.selected:
            offset = self.selection.offset
            pygame.draw.rect(self.display_surf, (255, 0, 0), (self.rect.left - offset.x, self.rect.top + 10 - offset.y,
                                                              self.rect.width, 10))
            pygame.draw.rect(self.display_surf, (0, 255, 0), (self.rect.left - offset.x, self.rect.top + 10 - offset.y,
                                                              self.rect.width * (self.health / self.max_health), 10))

    def import_assets(self, path):
        root_dir = Path(path)
        self.animations = {}
        for path in root_dir.iterdir():
            self.animations[str(path).split('\\')[-1]] = \
                [pygame.image.load(file).convert_alpha() for file in Path(path).iterdir() if file.is_file()]

class Warrior1(Unit):
    def __init__(self, pos, groups, path, selection):
        super().__init__(pos, groups, path, selection)
        self.health = 100
        self.max_health = 200
        self.display_surf = pygame.display.get_surface()
        self.mouse_pos = self.pos

        self.moving = False

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def check_selection(self):
        mouse = pygame.mouse.get_pressed()
        if self.selection.selection_rect.colliderect(self.rect):
            self.selected = True
        elif self.selected and not mouse[0]:
            pass
        else:
            self.selected = False

    def move(self, dt):
        mouse = pygame.mouse.get_pressed()
        if mouse[2] and self.selected:
            self.moving = True
            self.mouse_pos = vector(pygame.mouse.get_pos()) + self.selection.offset
        if self.moving and self.mouse_pos != self.pos:
            distance = self.mouse_pos - self.pos
            direction = distance.normalize()
            movement = direction * self.speed * dt
            self.pos += movement
            self.rect.centerx = round(self.pos.x)
            self.rect.centery = round(self.pos.y)
        if abs(self.mouse_pos.x - self.pos.x) < 0.5 and abs(self.mouse_pos.y - self.pos.y) < 0.5:
            self.moving = False

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)

class Warrior2(Unit):
    def __init__(self, pos, groups, path, selection):
        super().__init__(pos, groups, path, selection)
        self.health = 100
        self.max_health = 200
        self.display_surf = pygame.display.get_surface()
        self.mouse_pos = self.pos

        self.moving = False

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def check_selection(self):
        mouse = pygame.mouse.get_pressed()
        if self.selection.selection_rect.colliderect(self.rect):
            self.selected = True
        elif self.selected and not mouse[0]:
            pass
        else:
            self.selected = False

    def move(self, dt):
        mouse = pygame.mouse.get_pressed()
        if mouse[2] and self.selected:
            self.moving = True
            self.mouse_pos = vector(pygame.mouse.get_pos()) + self.selection.offset
        if self.moving and self.mouse_pos != self.pos:
            distance = self.mouse_pos - self.pos
            direction = distance.normalize()
            movement = direction * self.speed * dt
            self.pos += movement
            self.rect.centerx = round(self.pos.x)
            self.rect.centery = round(self.pos.y)
        if abs(self.mouse_pos.x - self.pos.x) < 0.5 and abs(self.mouse_pos.y - self.pos.y) < 0.5:
            self.moving = False

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)

class Warrior3(Unit):
    def __init__(self, pos, groups, path, selection):
        super().__init__(pos, groups, path, selection)
        self.health = 100
        self.max_health = 200
        self.display_surf = pygame.display.get_surface()
        self.mouse_pos = self.pos

        self.moving = False

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def check_selection(self):
        mouse = pygame.mouse.get_pressed()
        if self.selection.selection_rect.colliderect(self.rect):
            self.selected = True
        elif self.selected and not mouse[0]:
            pass
        else:
            self.selected = False

    def move(self, dt):
        mouse = pygame.mouse.get_pressed()
        if mouse[2] and self.selected:
            self.moving = True
            self.mouse_pos = vector(pygame.mouse.get_pos()) + self.selection.offset
        if self.moving and self.mouse_pos != self.pos:
            distance = self.mouse_pos - self.pos
            direction = distance.normalize()
            movement = direction * self.speed * dt
            self.pos += movement
            self.rect.centerx = round(self.pos.x)
            self.rect.centery = round(self.pos.y)
        if abs(self.mouse_pos.x - self.pos.x) < 0.5 and abs(self.mouse_pos.y - self.pos.y) < 0.5:
            self.moving = False

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)
