import pygame
import sys
from random import choice
from Obstacle import Obstacle
from Player import Player
from Mechanics import Mechanics
import os
import webbrowser

pygame.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()
monitor_size = [info.current_w, info.current_h]

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
fullscreen = False

player = pygame.sprite.GroupSingle()
player.add(Player(screen_size))

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('images/sky.jpg').convert()
ground_surface = pygame.image.load('images/ground.png').convert_alpha()
vignette_surface = pygame.image.load('images/vignette.png').convert_alpha()
pause_surface = pygame.image.load('images/pause.png').convert_alpha()

game_over_sound = pygame.mixer.Sound('audio/game_over.ogg')
theme_sound = pygame.mixer.Sound('audio/theme.ogg')
theme_sound.set_volume(0.5)
game_over_sound.set_volume(0.5)

channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)

channel1.play(theme_sound, loops = -1)

pause_screen_drawn = False
music_muted = False
sounds_muted = False
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

mechanics = Mechanics(screen_size)

resize_time = 0

while True:

    mouse = pygame.mouse.get_pos() 

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
                pause_screen_drawn = False
                pause_time = pygame.time.get_ticks() - pause_time
                start_time += int(pause_time / 1000)
                pause_time = 0

        if event.type == pygame.MOUSEBUTTONDOWN and current_screen == 0: 
            #github
            if screen_size[0] * 0.34 <= mouse[0] <= (screen_size[0] * 0.34) + screen_size[0] * 0.32 and screen_size[1] * 0.05 <= mouse[1] <= (screen_size[1] * 0.05) + screen_size[1] * 0.06:
                url = "https://github.com/f4rys"
                webbrowser.open(url, new=0, autoraise=True)

        if event.type == pygame.MOUSEBUTTONDOWN and current_screen == 1: 
            if screen_size[0] * 0.867 <= mouse[0] <= (screen_size[0] * 0.867) + screen_size[0] * 0.1 and screen_size[1] // 60 <= mouse[1] <= (screen_size[1] // 60) + screen_size[1] * 0.1:
                pause_time = pygame.time.get_ticks()
                current_screen = 2

        elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == 2:
            #esc
            if screen_size[0] * 0.867 <= mouse[0] <= (screen_size[0] * 0.867) + screen_size[0] * 0.1 and screen_size[1] // 60 <= mouse[1] <= (screen_size[1] // 60) + screen_size[1] * 0.1:
                current_screen = 1
                pause_screen_drawn = False
                pause_time = pygame.time.get_ticks() - pause_time
                start_time += int(pause_time / 1000)
                pause_time = 0
            #fullscreen
            if screen_size[0] * 0.373 <= mouse[0] <= (screen_size[0] * 0.373) + screen_size[0] * 0.254 and screen_size[1] * 0.47 <= mouse[1] <= (screen_size[1] * 0.47) + screen_size[1] * 0.06 and not fullscreen:
                screen = pygame.display.set_mode(monitor_size, pygame.RESIZABLE)
                fullscreen = True
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size=monitor_size, w=monitor_size[0], h=monitor_size[1]))
            elif screen_size[0] * 0.373 <= mouse[0] <= (screen_size[0] * 0.373) + screen_size[0] * 0.254 and screen_size[1] * 0.47 <= mouse[1] <= (screen_size[1] * 0.47) + screen_size[1] * 0.06 and fullscreen:
                screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, size=(1280,720), w=1280, h=720))
                fullscreen = False
            #reset best score
            if screen_size[0] * 0.32 <= mouse[0] <= (screen_size[0] * 0.32) + screen_size[0] * 0.36 and screen_size[1] * 0.57 <= mouse[1] <= (screen_size[1] * 0.57) + screen_size[1] * 0.06:
                mechanics.reset_best_score()
            #mute music
            if screen_size[0] * 0.38 <= mouse[0] <= (screen_size[0] * 0.38) + screen_size[0] * 0.241 and screen_size[1] * 0.67 <= mouse[1] <= (screen_size[1] * 0.67) + screen_size[1] * 0.06 and not music_muted:
                channel1.pause()
                music_muted = True
            elif screen_size[0] * 0.38 <= mouse[0] <= (screen_size[0] * 0.38) + screen_size[0] * 0.241 and screen_size[1] * 0.67 <= mouse[1] <= (screen_size[1] * 0.67) + screen_size[1] * 0.06 and music_muted:
                channel1.unpause()
                music_muted = False
            #mute sounds
            if screen_size[0] * 0.375 <= mouse[0] <= (screen_size[0] * 0.375) + screen_size[0] * 0.36 and screen_size[1] * 0.77 <= mouse[1] <= (screen_size[1] * 0.77) + screen_size[1] * 0.06 and not sounds_muted:
                channel2.set_volume(0)
                sounds_muted = True
            elif screen_size[0] * 0.375 <= mouse[0] <= (screen_size[0] * 0.375) + screen_size[0] * 0.36 and screen_size[1] * 0.77 <= mouse[1] <= (screen_size[1] * 0.77) + screen_size[1] * 0.06 and sounds_muted:
                channel2.set_volume(1)
                sounds_muted = False

        if event.type == obstacle_timer and current_screen == 1 and pygame.time.get_ticks() - resize_time > 1000:
            resize_time = 0
            obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2']), screen_size))

        if event.type == pygame.VIDEORESIZE:

            if(current_screen == 1):
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
        screen.blit(pygame.transform.scale(vignette_surface, screen_size), (0, 0))

        github_text = game_font.render("[VISIT MY GITHUB]", False, "White")
        github_text_rect = github_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 12))

        game_message = game_font.render("START THE GAME BY PRESSING 'SPACE'", False, "White")
        game_message_rectangle = game_message.get_rect(center=(screen_size[0] // 2, screen_size[1] // 1.25))

        screen.blit(github_text, github_text_rect)

        score_message = game_font.render(f"YOUR SCORE: {score}", False, "White")
        best_score_message = game_font.render(f"BEST_SCORE: {best_score}", False, "White")
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

        esc_message = game_font.render("[ESC]", False, "White")
        esc_message_rectangle = esc_message.get_rect(center=(screen_size[0] - screen_size[0] // 12, screen_size[1] // 14))

        player.draw(screen)
        player.update(channel2)

        obstacle_group.draw(screen)
        obstacle_group.update()

        screen.blit(pygame.transform.scale(vignette_surface, screen_size), (0, 0))
        screen.blit(esc_message, esc_message_rectangle)

        score = mechanics.display_score(game_font, start_time, screen)
        current_screen = mechanics.collision_sprite(player, obstacle_group, game_over_sound, channel2, score)

    elif current_screen == 2:
        screen.blit(pygame.transform.scale(pause_surface, screen_size), (0, 0))

        best_score = mechanics.load_best_score()

        esc_message = game_font.render("[ESC]", False, "White")
        esc_message_rectangle = esc_message.get_rect(center=(screen_size[0] - screen_size[0] // 12, screen_size[1] // 14))

        pause_text = game_font.render("GAME PAUSED", False, "White")
        fullscreen_text = game_font.render("[FULLSCREEN]", False, "White")
        best_score_text = game_font.render(f"BEST SCORE: {best_score}", False, "White")
        reset_best_score_text = game_font.render("[RESET BEST SCORE]", False, "White")

        if music_muted:
            mute_music_text = game_font.render("[UNMUTE MUSIC]", False, "White")
        else:
            mute_music_text = game_font.render("[MUTE MUSIC]", False, "White")

        if sounds_muted:
            mute_sound_text = game_font.render("[UNMUTE SOUND]", False, "White")
        else:
            mute_sound_text = game_font.render("[MUTE SOUND]", False, "White")

        pause_text_rect = pause_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 4))
        best_score_text_rect = best_score_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 4 + (screen_size[1] // 10) * 1))
        fullscreen_text_rect = fullscreen_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

        reset_best_score_text_rect = reset_best_score_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + (screen_size[1] // 10) * 1))
        mute_music_text_rect  = mute_music_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + (screen_size[1] // 10) * 2))
        mute_sound_text_rect = mute_sound_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2 + (screen_size[1] // 10) * 3))

        screen.blit(esc_message, esc_message_rectangle)       
        screen.blit(pause_text, pause_text_rect)
        screen.blit(best_score_text, best_score_text_rect)

        screen.blit(fullscreen_text, fullscreen_text_rect)
        screen.blit(reset_best_score_text, reset_best_score_text_rect)
        screen.blit(mute_music_text, mute_music_text_rect)
        screen.blit(mute_sound_text, mute_sound_text_rect)

    pygame.display.update()
    clock.tick(60)