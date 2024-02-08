import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super().__init__()
        self.screen_size = screen_size
        self.run_index = 0
        self.jump_index = 0
        self.load()
        
        
    def load(self):
        player_run1 = pygame.image.load('images/run1.png').convert_alpha()
        player_run2 = pygame.image.load('images/run2.png').convert_alpha()
        player_run3 = pygame.image.load('images/run3.png').convert_alpha()
        self.player_run = [player_run1, player_run2, player_run3]

        player_jump1 = pygame.image.load('images/jump1.png').convert_alpha()
        player_jump2 = pygame.image.load('images/jump2.png').convert_alpha()
        self.player_jump = [player_jump1, player_jump2]

        self.multiplier = self.screen_size[1] * 0.0015

        self.player_run = [pygame.transform.scale(img, (img.get_width() * self.multiplier, img.get_height() * self.multiplier)) for img in self.player_run]
        self.player_jump = [pygame.transform.scale(img, (img.get_width() * self.multiplier, img.get_height() * self.multiplier)) for img in self.player_jump]

        initial_x = self.screen_size[0] // 10
        initial_y = self.screen_size[1] - self.screen_size[1] // 2

        self.image = self.player_run[0]
        self.rect = self.image.get_rect(midbottom=(initial_x, initial_y))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.ogg')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.screen_size[1] - self.screen_size[1] // 3.5:
            self.gravity = -0.02548 * self.screen_size[1] - 5.849
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.screen_size[1] - self.screen_size[1] // 3.5:
            self.rect.bottom = self.screen_size[1] - self.screen_size[1] // 3.5

    def animation_state(self):
        if self.rect.bottom < self.screen_size[1] - self.screen_size[1] // 3.5:
            self.jump_index += 0.1
            if self.jump_index >= len(self.player_jump):
                self.jump_index = 0
            self.image = self.player_jump[int(self.jump_index)]
        else:
            self.run_index += 0.1
            if self.run_index >= len(self.player_run):
                self.run_index = 0
            self.image = self.player_run[int(self.run_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        self.load()