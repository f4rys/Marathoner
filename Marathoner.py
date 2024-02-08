import pygame
import sys
from random import choice
from Obstacle import Obstacle
from Player import Player
from Mechanics import Mechanics

pygame.init()
screen_size = (1280, 720)
aspect_ratio = 1280 / 720
screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption("Marathoner")
pygame.display.set_icon(pygame.image.load('icon.png'))
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/pixeled.ttf', (screen_size[0]+screen_size[1]) // 70)
game_active = False
start_time = 0
score = 0
current_screen = 0
pause_time = 0

player = pygame.sprite.GroupSingle()
player.add(Player(screen_size))

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('images/sky.jpg').convert()
ground_surface = pygame.image.load('images/ground.png').convert_alpha()

game_over_sound = pygame.mixer.Sound('audio/game_over.ogg')
theme_sound = pygame.mixer.Sound('audio/theme.ogg')
theme_sound.set_volume(0.5)
theme_sound.play(loops=-1)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

mechanics = Mechanics(screen_size)

resize_time = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_screen == 0:
                current_screen = 1
                start_time = int(pygame.time.get_ticks() / 1000)
            if event.key == pygame.K_ESCAPE and current_screen != 2:
                pause_time = pygame.time.get_ticks()
                current_screen = 2
            elif event.key == pygame.K_ESCAPE and current_screen == 2:
                current_screen = 1
                pause_time = pygame.time.get_ticks() - pause_time
                start_time += int(pause_time / 1000)
                pause_time = 0

        if event.type == obstacle_timer and current_screen == 1 and pygame.time.get_ticks() - resize_time > 1000:
            resize_time = 0
            obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2']), screen_size))

        if event.type == pygame.VIDEORESIZE:
            current_screen = 2
            pause_time = pygame.time.get_ticks()
            resize_time = pygame.time.get_ticks()

            new_aspect_ratio = event.w / event.h

            if new_aspect_ratio < 1.6 or new_aspect_ratio > 1.9:
                new_width = event.w
                new_height = int(new_width / aspect_ratio)
                screen_size = (new_width, new_height)
            else:
                screen_size = event.size

            game_font = pygame.font.Font('fonts/pixeled.ttf', (screen_size[0]+screen_size[1]) // 70)
            screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
            player.sprite.update_screen_size(screen_size)
            mechanics.update_screen_size(screen_size)

            for obstacle in obstacle_group:
                obstacle.update_screen_size(screen_size)

    if current_screen == 0:
        best_score = mechanics.load_best_score()
        screen.blit(pygame.transform.scale(sky_surface, screen_size), (0, 0))

        game_message = game_font.render("Start the game by pressing 'space'", False, "White")
        game_message_rectangle = game_message.get_rect(center=(screen_size[0] // 2, screen_size[1] // 1.25))

        score_message = game_font.render(f"Your score: {score}", False, "White")
        best_score_message = game_font.render(f"Best score: {best_score}", False, "White")
        score_message_rectangle = score_message.get_rect(center=(screen_size[0] // 2, screen_size[1] // 1.25))
        best_score_message_rectangle = best_score_message.get_rect(center=(screen_size[0] // 2, screen_size[1] // 1.1))

        if score == 0:
            screen.blit(game_message, game_message_rectangle)
            screen.blit(best_score_message, best_score_message_rectangle)
        else:
            screen.blit(score_message, score_message_rectangle)
            screen.blit(best_score_message, best_score_message_rectangle)
    
    elif current_screen == 1:
        screen.blit(pygame.transform.scale(sky_surface, screen_size), (0, 0))
        screen.blit(pygame.transform.scale(ground_surface, screen_size), (0, screen_size[1] * 0.6))
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        score = mechanics.display_score(game_font, start_time, screen)

        current_screen = mechanics.collision_sprite(player, obstacle_group, game_over_sound, score)

    elif current_screen == 2:
        screen.fill((0, 0, 0))
        marathoner_text = game_font.render("Marathoner", False, "White")
        marathoner_text_rect = marathoner_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))
        screen.blit(marathoner_text, marathoner_text_rect)     

    pygame.display.update()
    clock.tick(60)