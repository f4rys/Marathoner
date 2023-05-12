import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'stone1':
            image = pygame.image.load('graphics/stone1.png').convert_alpha()
            y_pos = 520
        else:
            image = pygame.image.load('graphics/stone2.png').convert_alpha()
            y_pos = 350

        self.image = image
        self.rect = self.image.get_rect(midbottom = (randint(1300,1600), y_pos))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()