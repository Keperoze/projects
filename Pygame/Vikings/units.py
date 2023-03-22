import pygame
from pygame.math import Vector2 as vector
from pathlib import Path
from debug import debug
from statistics import mean

class Unit(pygame.sprite.Sprite):
    def __init__(self, pos, groups, path, selection):
        super().__init__(groups)

        self.import_assets(path)
        self.frame_index = 0
        self.status = 'idle'

        self.previous_pos = []
        self.last_pos_time = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.speed = 200

        self.hitbox = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)
        self.health = 100
        self.max_health = 200
        self.selected = False
        self.selection = selection
        self.display_surf = pygame.display.get_surface()
        self.moving = False
        self.mouse_pos = self.pos

    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount

    def get_health(self, amount):
        if self.health < self.max_health:
            self.health += amount

    def check_selection(self):
        mouse = pygame.mouse.get_pressed()
        if self.selection.selection_rect.colliderect(self.rect) or \
                (mouse[0] and self.hitbox.collidepoint(vector(pygame.mouse.get_pos()) + self.selection.offset)):
            self.selected = True
        elif self.selected and not mouse[0]:
            pass
        else:
            self.selected = False

    def basic_health(self):
        if self.selected:
            offset = self.selection.offset
            pygame.draw.rect(self.display_surf, (210, 43, 43), (self.hitbox.left - offset.x, self.hitbox.bottom - 50 - offset.y,
                                                              self.hitbox.width, 8))
            pygame.draw.rect(self.display_surf, (4, 204, 130), (self.hitbox.left - offset.x, self.hitbox.bottom - 50 - offset.y,
                                                              self.hitbox.width * (self.health / self.max_health), 8))

    def move(self, dt):
        mouse = pygame.mouse.get_pressed()
        if mouse[2] and self.selected:
            self.moving = True
            if self.direction[0] > 0:
                self.status = 'run'
            else:
                self.status = 'run_l'
            self.mouse_pos = vector(pygame.mouse.get_pos()) + self.selection.offset
        if self.moving and self.mouse_pos != self.pos:
            distance = self.mouse_pos - self.pos
            self.direction = distance.normalize()
            movement = self.direction * self.speed * dt
            self.pos.x += movement.x
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.collision('horizontal')

            self.pos.y += movement.y
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            self.collision('vertical')

        if abs(self.mouse_pos.x - self.pos.x) < 0.5 and abs(self.mouse_pos.y - self.pos.y) < 0.5:
            self.moving = False
            if self.direction[0] > 0:
                self.status = 'idle'
            else:
                self.status = 'idle_l'

    def check_movement(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pos_time > 100:
            self.previous_pos.append(self.rect.center)
            self.last_pos_time = current_time
            if len(self.previous_pos) >= 4:
                self.previous_pos = self.previous_pos[1:]
                if abs(mean(t[0] for t in self.previous_pos) - self.previous_pos[0][0]) + \
                        abs(mean(t[1] for t in self.previous_pos) - self.previous_pos[0][1]) < 0.5:
                    self.moving = False
                    self.status = 'idle'
                    self.previous_pos = []

    def collision(self, direction):
        for sprite in self.selection.sprites():
            if sprite != self and sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving to right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def animate(self, dt):
        current_animation = self.animations[self.status]
        self.frame_index += 8 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

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
        self.speed = 200

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)
        if self.moving:
            self.check_movement()
        debug(self.direction)

class Warrior2(Unit):
    def __init__(self, pos, groups, path, selection):
        super().__init__(pos, groups, path, selection)
        self.health = 100
        self.max_health = 200
        self.speed = 150

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)
        if self.moving:
            self.check_movement()

class Warrior3(Unit):
    def __init__(self, pos, groups, path, selection):
        super().__init__(pos, groups, path, selection)
        self.health = 100
        self.max_health = 200
        self.speed = 150

    def update(self, dt):
        self.animate(dt)
        self.check_selection()
        self.basic_health()
        self.move(dt)
        if self.moving:
            self.check_movement()
