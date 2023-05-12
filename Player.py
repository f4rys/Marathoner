import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_run1 = pygame.image.load('graphics/player1.png').convert_alpha()
        player_run2 = pygame.image.load('graphics/player2.png').convert_alpha()
        self.player_run = [player_run1, player_run2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player2.png').convert_alpha()

        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (180, 520))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audios/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 520:
            self.gravity = -25
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 520:
            self.rect.bottom = 520

    def animation_state(self):
        if self.rect.bottom < 520:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_run):
                self.player_index = 0
            self.image = self.player_run[int(self.player_index)]
        
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()