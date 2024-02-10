import os
import sys
import webbrowser
from random import choice
import pygame
from Obstacle import Obstacle
from Player import Player
from Mechanics import Mechanics

class Game():
    def __init__(self):
        pygame.init()

        # CURRENT MONITOR
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        info = pygame.display.Info()
        self.monitor_size = [info.current_w, info.current_h]

        # WINDOW SETTINGS
        self.original_screen_size = (int(info.current_w / 1.5), int(info.current_h / 1.5))
        self.screen_size = self.original_screen_size
        self.aspect_ratio = self.screen_size[0] / self.screen_size[1]

        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        pygame.display.set_caption("Marathoner")
        pygame.display.set_icon(pygame.image.load('icon.png'))

        # PLAYER
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.screen_size))

        # OBSTACLES
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

        # SURFACES
        self.sky_surface = pygame.image.load('images/sky.jpg').convert()
        self.ground_surface = pygame.image.load('images/ground.png').convert_alpha()
        self.vignette_surface = pygame.image.load('images/vignette.png').convert_alpha()
        self.pause_surface = pygame.image.load('images/pause.png').convert_alpha()

        # MUSIC & SOUNDS
        self.game_over_sound = pygame.mixer.Sound('audio/game_over.ogg')
        theme_sound = pygame.mixer.Sound('audio/theme.ogg')

        self.game_over_sound.set_volume(0.5)
        theme_sound.set_volume(0.5)

        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)

        self.channel1.play(theme_sound, loops = -1)

        # CLOCK
        self.clock = pygame.time.Clock()

        # FONT
        self.game_font = pygame.font.Font('fonts/pixeled.ttf', (self.screen_size[0] + self.screen_size[1]) // 70)

        # MECHANICS
        self.mechanics = Mechanics(self.screen_size)

        # VARIABLES
        self.start_time = 0
        self.score = 0
        self.current_screen = 0
        self.pause_time = 0
        self.resize_time = 0

        # FLAGS
        self.game_active = False
        self.fullscreen = False
        self.music_muted = False
        self.sounds_muted = False

    def toggle_fullscreen(self):
        # ENTER FULLSCREEN MODE
        if not self.fullscreen:
            self.screen = pygame.display.set_mode(self.monitor_size, pygame.RESIZABLE)
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, w=self.monitor_size[0], h=self.monitor_size[1]))
            self.fullscreen = True
        # LEAVE FULLSCREEN MODE
        elif self.fullscreen:
            self.screen = pygame.display.set_mode((self.original_screen_size[0], self.original_screen_size[1]), pygame.RESIZABLE)
            pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, w=self.original_screen_size[0], h=self.original_screen_size[1]))
            self.fullscreen = False

    def run(self):
        # GAME LOOP
        while True:

            # GET MOUSE POSITION
            mouse = pygame.mouse.get_pos()

            # LOAD BEST SCORE
            best_score = self.mechanics.load_best_score()

            # EVENT HANDLING
            for event in pygame.event.get():
                # QUIT GAME
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # START GAME
                    if event.key == pygame.K_SPACE and self.current_screen == 0:
                        self.current_screen = 1
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                    # OPEN PAUSE MENU THROUGH ESC
                    if event.key == pygame.K_ESCAPE and self.current_screen != 2:
                        self.pause_time = pygame.time.get_ticks()
                        self.current_screen = 2
                    # RETURN FROM PAUSE MENU THROUGH ESC
                    elif event.key == pygame.K_ESCAPE and self.current_screen == 2:
                        self.current_screen = 1
                        self.pause_time = pygame.time.get_ticks() - self.pause_time
                        self.start_time += int(self.pause_time / 1000)
                        self.pause_time = 0

                if event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == 0: 
                    # OPEN GITHUB
                    if self.screen_size[0] * 0.34 <= mouse[0] <= (self.screen_size[0] * 0.34) + self.screen_size[0] * 0.32 and self.screen_size[1] * 0.05 <= mouse[1] <= (self.screen_size[1] * 0.05) + self.screen_size[1] * 0.06:
                        url = "https://github.com/f4rys"
                        webbrowser.open(url, new=0, autoraise=True)

                if event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == 1: 
                    # OPEN PAUSE MENU THROUGH INGAME BUTTON
                    if self.screen_size[0] * 0.867 <= mouse[0] <= (self.screen_size[0] * 0.867) + self.screen_size[0] * 0.1 and self.screen_size[1] // 60 <= mouse[1] <= (self.screen_size[1] // 60) + self.screen_size[1] * 0.1:
                        self.pause_time = pygame.time.get_ticks()
                        self.current_screen = 2

                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == 2:
                    # RETURN FROM PAUSE MENU THROUGH INGAME BUTTON
                    if self.screen_size[0] * 0.867 <= mouse[0] <= (self.screen_size[0] * 0.867) + self.screen_size[0] * 0.1 and self.screen_size[1] // 60 <= mouse[1] <= (self.screen_size[1] // 60) + self.screen_size[1] * 0.1:
                        self.current_screen = 1
                        self.pause_time = pygame.time.get_ticks() - self.pause_time
                        self.start_time += int(self.pause_time / 1000)
                        self.pause_time = 0
                    # FULLSCREEN
                    if self.screen_size[0] * 0.373 <= mouse[0] <= (self.screen_size[0] * 0.373) + self.screen_size[0] * 0.254 and self.screen_size[1] * 0.47 <= mouse[1] <= (self.screen_size[1] * 0.47) + self.screen_size[1] * 0.06:
                        self.toggle_fullscreen()
                    # RESET BEST SCORE
                    if self.screen_size[0] * 0.32 <= mouse[0] <= (self.screen_size[0] * 0.32) + self.screen_size[0] * 0.36 and self.screen_size[1] * 0.57 <= mouse[1] <= (self.screen_size[1] * 0.57) + self.screen_size[1] * 0.06:
                        self.mechanics.reset_best_score()
                    # MUTE MUSIC
                    if self.screen_size[0] * 0.38 <= mouse[0] <= (self.screen_size[0] * 0.38) + self.screen_size[0] * 0.241 and self.screen_size[1] * 0.67 <= mouse[1] <= (self.screen_size[1] * 0.67) + self.screen_size[1] * 0.06 and not self.music_muted:
                        self.channel1.pause()
                        self.music_muted = True
                    # UNMUTE MUSIC
                    elif self.screen_size[0] * 0.38 <= mouse[0] <= (self.screen_size[0] * 0.38) + self.screen_size[0] * 0.241 and self.screen_size[1] * 0.67 <= mouse[1] <= (self.screen_size[1] * 0.67) + self.screen_size[1] * 0.06 and self.music_muted:
                        self.channel1.unpause()
                        self.music_muted = False
                    # MUTE SOUNDS
                    if self.screen_size[0] * 0.375 <= mouse[0] <= (self.screen_size[0] * 0.375) + self.screen_size[0] * 0.36 and self.screen_size[1] * 0.77 <= mouse[1] <= (self.screen_size[1] * 0.77) + self.screen_size[1] * 0.06 and not self.sounds_muted:
                        self.channel2.set_volume(0)
                        self.sounds_muted = True
                    # UNMUTE SOUNDS
                    elif self.screen_size[0] * 0.375 <= mouse[0] <= (self.screen_size[0] * 0.375) + self.screen_size[0] * 0.36 and self.screen_size[1] * 0.77 <= mouse[1] <= (self.screen_size[1] * 0.77) + self.screen_size[1] * 0.06 and self.sounds_muted:
                        self.channel2.set_volume(1)
                        self.sounds_muted = False

                # ADD NEW OBSTACLE
                if event.type == self.obstacle_timer and self.current_screen == 1 and pygame.time.get_ticks() - self.resize_time > 1000:
                    self.resize_time = 0
                    self.obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2']), self.screen_size))

                # WHEN RESIZING WINDOW
                if event.type == pygame.VIDEORESIZE:
                    
                    # PAUSE GAME
                    if(self.current_screen == 1):
                        self.current_screen = 2
                        self.pause_time = pygame.time.get_ticks()
                        self.resize_time = pygame.time.get_ticks()

                    # FORBID CHANGING ASPECT RATIO
                    new_aspect_ratio = event.w / event.h

                    if new_aspect_ratio < 1.6 or new_aspect_ratio > 1.9:
                        new_width = event.w
                        new_height = int(new_width / self.aspect_ratio)
                        self.screen_size = (new_width, new_height)
                    else:
                        self.screen_size = (event.w, event.h)

                    # RESIZE GAME FONT
                    self.game_font = pygame.font.Font('fonts/pixeled.ttf', (self.screen_size[0] + self.screen_size[1]) // 70)

                    # RESIZE SCREEN
                    self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

                    # RESIZE PLAYER
                    self.player.sprite.update_screen_size(self.screen_size)

                    # RESIZE SCORE rectS
                    self.mechanics.update_screen_size(self.screen_size)

                    # RESIZE OBSTACLES
                    for obstacle in self.obstacle_group:
                        obstacle.update_screen_size(self.screen_size)

            # START / GAME OVER MENU
            if self.current_screen == 0:

                # SHOW SCORE AFTER LOSING A GAME, 'START THE GAME' MESSAGE INSTEAD
                if self.score == 0:
                    game_message = self.game_font.render("START THE GAME BY PRESSING 'SPACE'", False, "White")

                else:
                    game_message = self.game_font.render(f"YOUR SCORE: {self.score}", False, "White")

                # RENDERS AND RECTANGLES
                github_text = self.game_font.render("[VISIT MY GITHUB]", False, "White")
                best_score_message = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")

                github_text_rect = github_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 12))
                best_score_message_rect = best_score_message.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 1.1))
                game_message_rect = game_message.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 1.25))

                # DRAW ELEMENTS
                self.screen.blit(pygame.transform.scale(self.sky_surface, self.screen_size), (0, 0))
                self.screen.blit(pygame.transform.scale(self.vignette_surface, self.screen_size), (0, 0))
                self.screen.blit(best_score_message, best_score_message_rect)
                self.screen.blit(github_text, github_text_rect)
                self.screen.blit(game_message, game_message_rect)

            # GAME
            elif self.current_screen == 1:

                # DRAW BACKGROUND
                self.screen.blit(pygame.transform.scale(self.sky_surface, self.screen_size), (0, 0))
                self.screen.blit(pygame.transform.scale(self.ground_surface, self.screen_size), (0, self.screen_size[1] * 0.6))

                # DRAW PLAYER AND OBSTACLES
                self.player.draw(self.screen)
                self.player.update(self.channel2)

                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                # DRAW VIGNETTE
                self.screen.blit(pygame.transform.scale(self.vignette_surface, self.screen_size), (0, 0))

                # DRAW [ESC] BUTTON
                esc_message = self.game_font.render("[ESC]", False, "White")
                esc_message_rect = esc_message.get_rect(center=(self.screen_size[0] - self.screen_size[0] // 12, self.screen_size[1] // 14))
                self.screen.blit(esc_message, esc_message_rect)

                # DRAW SCORE
                self.score = self.mechanics.display_score(self.game_font, self.start_time, self.screen)

                # CHECK FOR COLLISIONS
                self.current_screen = self.mechanics.collision_sprite(self.player, self.obstacle_group, self.game_over_sound, self.channel2, self.score)

            # PAUSE MENU
            elif self.current_screen == 2:

                # RENDERS
                if self.music_muted:
                    mute_music_text = self.game_font.render("[UNMUTE MUSIC]", False, "White")
                else:
                    mute_music_text = self.game_font.render("[MUTE MUSIC]", False, "White")

                if self.sounds_muted:
                    mute_sound_text = self.game_font.render("[UNMUTE SOUND]", False, "White")
                else:
                    mute_sound_text = self.game_font.render("[MUTE SOUND]", False, "White")        

                esc_message = self.game_font.render("[ESC]", False, "White")
                pause_text = self.game_font.render("GAME PAUSED", False, "White")
                fullscreen_text = self.game_font.render("[FULLSCREEN]", False, "White")
                best_score_text = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")
                reset_best_score_text = self.game_font.render("[RESET BEST SCORE]", False, "White")

                # RECTANGLES
                esc_message_rect = esc_message.get_rect(center=(self.screen_size[0] - self.screen_size[0] // 12, self.screen_size[1] // 14))
                pause_text_rect = pause_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 4))
                best_score_text_rect = best_score_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 4 + (self.screen_size[1] // 10) * 1))
                fullscreen_text_rect = fullscreen_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
                reset_best_score_text_rect = reset_best_score_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 1))
                mute_music_text_rect  = mute_music_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 2))
                mute_sound_text_rect = mute_sound_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 3))

                # DRAW ELEMENTS
                self.screen.blit(pygame.transform.scale(self.pause_surface, self.screen_size), (0, 0))
                self.screen.blit(esc_message, esc_message_rect)       
                self.screen.blit(pause_text, pause_text_rect)
                self.screen.blit(best_score_text, best_score_text_rect)
                self.screen.blit(fullscreen_text, fullscreen_text_rect)
                self.screen.blit(reset_best_score_text, reset_best_score_text_rect)
                self.screen.blit(mute_music_text, mute_music_text_rect)
                self.screen.blit(mute_sound_text, mute_sound_text_rect)

            pygame.display.update()
            self.clock.tick(60)