from random import randint

import pygame

from resource_path import resource_path

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type, screen_size):
        super().__init__()

        self.screen_size = screen_size
        self.type = obstacle_type
        self.load()

    def load(self, initial=True):
        if self.type == 'stone1':
            image = pygame.image.load(resource_path('images/stone1.png')).convert_alpha()
            y_pos = self.screen_size[1] * 0.74
        else:
            image = pygame.image.load(resource_path('images/stone2.png')).convert_alpha()
            y_pos = self.screen_size[1] * 0.49

        multiplier = self.screen_size[1] * 0.0015

        self.image = pygame.transform.scale(image, (image.get_width() * multiplier, image.get_height() * multiplier))
        self.mask = pygame.mask.from_surface(self.image)

        if initial:
            self.rect = self.image.get_rect(midbottom=(randint(self.screen_size[0], self.screen_size[0] + self.screen_size[0] // 4), y_pos))
        else:
            self.rect = self.image.get_rect(midbottom=(self.rect.x, y_pos))
    def update(self):
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= - (self.screen_size[0] + 50):
            self.kill()

    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        self.load(False)
