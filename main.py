import pygame
import sys
from random import randint, choice

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

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = game_font.render(str(current_time) + " s", False, 'White')
    score_rectangle = score_surface.get_rect(center=(640, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        game_over_sound.play()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Marathoner")
pygame.display.set_icon(pygame.image.load('icon.png'))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/pixeled.ttf', 30)
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/sky.jpg').convert()
ground_surface = pygame.image.load('graphics/ground.jpg').convert()

game_message = game_font.render("Start the game by pressing 'space'", False, "White")
game_message_rectangle = game_message.get_rect(center=(640, 600))

game_over_sound = pygame.mixer.Sound('audios/game_over.mp3')
theme_sound = pygame.mixer.Sound('audios/theme.mp3')
theme_sound.set_volume(0.5)
theme_sound.play(loops = -1)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and game_active == False:
            if event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2'])))

    if game_active:

        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,520))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = display_score()

        game_active = collision_sprite()

    else:
        screen.blit(sky_surface, (0,0))
        
        score_message = game_font.render(f"Your score: {score}", False, "White")
        score_message_rectangle = score_message.get_rect(center=(640, 600))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)

    pygame.display.update()
    clock.tick(60)