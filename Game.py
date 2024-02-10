import os
import sys
import webbrowser
from random import choice
import pygame
from Obstacle import Obstacle
from Player import Player
from ScoreSystem import ScoreSystem
from Button import Button

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
        self.game_font = pygame.font.Font('font/pixeled.ttf', (self.screen_size[0] + self.screen_size[1]) // 70)

        # SCORE SYSTEM
        self.score_system = ScoreSystem(self.screen_size)

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
            self.handle_resize(self.monitor_size[0], self.monitor_size[1])
            self.fullscreen = True
        # LEAVE FULLSCREEN MODE
        elif self.fullscreen:
            self.screen = pygame.display.set_mode((self.original_screen_size[0], self.original_screen_size[1]), pygame.RESIZABLE)
            self.handle_resize(self.original_screen_size[0], self.original_screen_size[1])
            self.fullscreen = False

    def toggle_music(self):
        # MUTE MUSIC
        if not self.music_muted:
            self.channel1.pause()
            self.music_muted = True
        # UNMUTE MUSIC
        elif self.music_muted:
            self.channel1.unpause()
            self.music_muted = False

    def toggle_sounds(self):
        # MUTE SOUNDS
        if not self.sounds_muted:
            self.channel2.set_volume(0)
            self.sounds_muted = True
        # UNMUTE SOUNDS
        elif self.sounds_muted:
            self.channel2.set_volume(1)
            self.sounds_muted = False

    def start_game(self):
        self.current_screen = 1
        self.start_time = int(pygame.time.get_ticks() / 1000)

    def pause_game(self):
        self.pause_time = pygame.time.get_ticks()
        self.current_screen = 2

    def resume_game(self):
        self.current_screen = 1
        self.pause_time = pygame.time.get_ticks() - self.pause_time
        self.start_time += int(self.pause_time / 1000)
        self.pause_time = 0

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def collision_sprite(self):
        # MASKS FOR PIXEL PERFECT COLLISION DETECTION
        if pygame.sprite.spritecollideany(self.player.sprite, self.obstacle_group, pygame.sprite.collide_mask):
            self.obstacle_group.empty()
            self.channel2.play(self.game_over_sound)
            self.score_system.save_best_score(self.score)
            return 0
        else:
            return 1
        
    def open_github(self):
        url = "https://github.com/f4rys"
        webbrowser.open(url, new=0, autoraise=True)

    def handle_resize(self, w, h):
        # PAUSE GAME
        if(self.current_screen == 1):
            self.current_screen = 2
            self.pause_time = pygame.time.get_ticks()
            self.resize_time = pygame.time.get_ticks()

        # FORBID CHANGING ASPECT RATIO
        new_aspect_ratio = w / h

        if new_aspect_ratio < 1.6 or new_aspect_ratio > 1.9:
            new_width = w
            new_height = int(new_width / self.aspect_ratio)
            self.screen_size = (new_width, new_height)
        else:
            self.screen_size = (w, h)

        # RESIZE GAME FONT
        self.game_font = pygame.font.Font('font/pixeled.ttf', (self.screen_size[0] + self.screen_size[1]) // 70)

        # RESIZE SCREEN
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

        # RESIZE PLAYER
        self.player.sprite.update_screen_size(self.screen_size)

        # RESIZE SCORE rectS
        self.score_system.update_screen_size(self.screen_size)

        # RESIZE OBSTACLES
        for obstacle in self.obstacle_group:
            obstacle.update_screen_size(self.screen_size)

    def run(self):
        # GAME LOOP
        while True:

            # GET MOUSE POSITION
            mouse = pygame.mouse.get_pos()

            # LOAD BEST SCORE
            best_score = self.score_system.load_best_score()

            # LOAD EVENTS
            events = pygame.event.get()

            # EVENT HANDLING
            for event in events:
                # QUIT GAME
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    # START GAME
                    if event.key == pygame.K_SPACE and self.current_screen == 0:
                        self.start_game()
                    # OPEN PAUSE MENU THROUGH ESC
                    if event.key == pygame.K_ESCAPE and self.current_screen == 1:
                        self.pause_game()
                    # RETURN FROM PAUSE MENU THROUGH ESC
                    elif event.key == pygame.K_ESCAPE and self.current_screen == 2:
                        self.resume_game()

                # ADD NEW OBSTACLE
                if event.type == self.obstacle_timer and self.current_screen == 1 and pygame.time.get_ticks() - self.resize_time > 1000:
                    self.resize_time = 0
                    self.obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2']), self.screen_size))

                # WHEN RESIZING WINDOW
                if event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event.w, event.h)

            # START / GAME OVER MENU
            if self.current_screen == 0:

                # SHOW SCORE AFTER LOSING A GAME, 'START THE GAME' MESSAGE INSTEAD
                if self.score == 0:
                    game_message = self.game_font.render("START THE GAME BY PRESSING 'SPACE'", False, "White")

                else:
                    game_message = self.game_font.render(f"YOUR SCORE: {self.score}", False, "White")

                # RENDERS AND RECTANGLES
                best_score_message = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")


                best_score_message_rect = best_score_message.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 1.1))
                game_message_rect = game_message.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 1.25))

                # DRAW ELEMENTS
                self.screen.blit(pygame.transform.scale(self.sky_surface, self.screen_size), (0, 0))
                self.screen.blit(pygame.transform.scale(self.vignette_surface, self.screen_size), (0, 0))
                self.screen.blit(best_score_message, best_score_message_rect)
                self.screen.blit(game_message, game_message_rect)
                Button(self.screen_size[0] // 2, self.screen_size[1] // 12, self.game_font, "[VISIT MY GITHUB]", self.screen, self.open_github, events).process()

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

                # DRAW SCORE
                self.score = self.score_system.display_score(self.game_font, self.start_time, self.screen)

                # CHECK FOR COLLISIONS
                self.current_screen = self.collision_sprite()

                # DRAW [ESC] BUTTON
                Button(self.screen_size[0] - self.screen_size[0] // 12, self.screen_size[1] // 14, self.game_font, "[ESC]", self.screen, self.pause_game, events).process()

            # PAUSE MENU
            elif self.current_screen == 2:

                # DRAW BACKGROUND
                self.screen.blit(pygame.transform.scale(self.sky_surface, self.screen_size), (0, 0))

                # RENDERS
                if self.music_muted:
                    music_message = "[UNMUTE MUSIC]"
                else:
                    music_message = "[MUTE MUSIC]"

                if self.sounds_muted:
                    sounds_message = "[UNMUTE SOUND]"
                else:
                    sounds_message = "[MUTE SOUND]"

                pause_text = self.game_font.render("GAME PAUSED", False, "White")
                best_score_text = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")

                # RECTANGLES
                pause_text_rect = pause_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 4))
                best_score_text_rect = best_score_text.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 4 + (self.screen_size[1] // 10) * 1))

                # DRAW ELEMENTS
                self.screen.blit(pygame.transform.scale(self.pause_surface, self.screen_size), (0, 0))      
                self.screen.blit(pause_text, pause_text_rect)
                self.screen.blit(best_score_text, best_score_text_rect)

                Button(self.screen_size[0] - self.screen_size[0] // 12, self.screen_size[1] // 14, self.game_font, "[ESC]", self.screen, self.resume_game, events).process()
                Button(self.screen_size[0] // 2, self.screen_size[1] // 2, self.game_font, "[FULLSCREEN]", self.screen, self.toggle_fullscreen, events).process()
                Button(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 1, self.game_font, "[RESET BEST SCORE]", self.screen, self.score_system.reset_best_score, events).process()
                Button(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 2, self.game_font, music_message, self.screen, self.toggle_music, events).process()
                Button(self.screen_size[0] // 2, self.screen_size[1] // 2 + (self.screen_size[1] // 10) * 3, self.game_font, sounds_message, self.screen, self.toggle_sounds, events).process()

            pygame.display.update()
            self.clock.tick(60)