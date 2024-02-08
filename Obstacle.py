import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, screen_size):
        super().__init__()

        self.screen_size = screen_size
        self.type = type
        self.load()

    def load(self):
        if self.type == 'stone1':
            image = pygame.image.load('images/stone1.png').convert_alpha()
            y_pos = self.screen_size[1] * 0.72
        else:
            image = pygame.image.load('images/stone2.png').convert_alpha()
            y_pos = self.screen_size[1] * 0.49

        multiplier = self.screen_size[1] * 0.0015

        image = pygame.transform.scale(image, (image.get_width() * multiplier, image.get_height() * multiplier))

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect(midbottom=(randint(self.screen_size[0], self.screen_size[0] + self.screen_size[0] // 4), y_pos))

    def update(self):
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= - (self.screen_size[0] + 50):
            self.kill()

    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        self.load()
