import pygame
import sys
from random import choice
from Obstacle import Obstacle
from Player import Player
from Mechanics import Mechanics

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

mechanics = Mechanics()

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

        score = mechanics.display_score(game_font, start_time, screen)

        game_active = mechanics.collision_sprite(player, obstacle_group, game_over_sound, score)

    else:
        best_score = mechanics.load_best_score()
        screen.blit(sky_surface, (0,0))
        
        score_message = game_font.render(f"Your score: {score}", False, "White")
        best_score_message = game_font.render(f"Best score: {best_score}", False, "White")
        score_message_rectangle = score_message.get_rect(center=(640, 600))
        best_score_message_rectangle = best_score_message.get_rect(center=(640, 660))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
            screen.blit(best_score_message, best_score_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)
            screen.blit(best_score_message, best_score_message_rectangle)

    pygame.display.update()
    clock.tick(60)