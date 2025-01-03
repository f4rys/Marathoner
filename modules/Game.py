import os
import sys
import webbrowser
from random import choice

import pygame

from modules.Obstacle import Obstacle
from modules.Player import Player
from modules.ScoreSystem import ScoreSystem
from modules.Button import Button
from modules.Settings import Settings

from modules.screens.StartGameScreen import StartGameScreen
from modules.screens.GameOverScreen import GameOverScreen
from modules.screens.PauseGameScreen import PauseGameScreen

from resource_path import resource_path

class Game():
    def __init__(self):
        pygame.init()

        # CREATE FOLDER TO STORE BEST SCORE IF NOT EXIST YET
        try:
            os.mkdir(os.path.expanduser("~") + '/Marathoner')
        except FileExistsError:
            pass

        # SETTINGS
        self.settings = Settings()

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
        pygame.display.set_icon(pygame.image.load(resource_path('images/icon.ico')))

        # PLAYER
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(self.screen_size))

        # OBSTACLES
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

        # SURFACES
        self.sky_surface = pygame.image.load(resource_path('images/sky.jpg')).convert()
        self.ground_surface = pygame.image.load(resource_path('images/ground.png')).convert_alpha()
        self.vignette_surface = pygame.image.load(resource_path('images/vignette.png')).convert_alpha()
        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

        # MUSIC & SOUNDS
        self.game_over_sound = pygame.mixer.Sound(resource_path('audio/game_over.ogg'))
        self.theme_sound = pygame.mixer.Sound(resource_path('audio/theme.ogg'))

        self.channel1 = pygame.mixer.Channel(0)
        self.channel2 = pygame.mixer.Channel(1)

        self.game_over_sound.set_volume(1)
        self.theme_sound.set_volume(1)

        self.channel2.set_volume(1 if self.settings.sounds else 0)
        self.channel1.set_volume(0.5 if self.settings.music else 0)

        self.channel1.play(self.theme_sound, loops = -1)

        # CLOCK
        self.clock = pygame.time.Clock()

        # FONT
        self.game_font = pygame.font.Font(resource_path('font/pixeled.ttf'), (self.screen_size[0] + self.screen_size[1]) // 70)

        # SCORE SYSTEM
        self.score_system = ScoreSystem(self.screen_size)

        # VARIABLES
        self.start_time = 0
        self.score = 0
        self.current_screen = 0
        self.pause_time = 0
        self.resize_time = 0
        self.last_game_over_time = 0

        # FLAGS
        self.game_active = False
        self.fullscreen = False

        # SCREENS
        self.start_game_screen = StartGameScreen(self.screen, self.game_font, self)
        self.game_over_screen = GameOverScreen(self.screen, self.game_font, self)
        self.pause_game_screen = PauseGameScreen(self.screen, self.game_font, self)

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
        self.settings.update_settings(not self.settings.music, "Music")

        if self.settings.music:
            self.channel1.set_volume(0.5)
        else:
            self.channel1.set_volume(0)

    def toggle_sounds(self):
        self.settings.update_settings(not self.settings.sounds, "Sounds")

        if self.settings.sounds:
            self.channel2.set_volume(1)
        else:
            self.channel2.set_volume(0)

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

    def abort_game(self):
        self.current_screen = 0
        self.score = 0
        self.obstacle_group.empty()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def collision_sprite(self):
        # MASKS FOR PIXEL PERFECT COLLISION DETECTION
        if pygame.sprite.spritecollideany(self.player.sprite, self.obstacle_group, pygame.sprite.collide_mask):
            self.obstacle_group.empty()
            self.channel2.play(self.game_over_sound)
            self.score_system.save_best_score(self.score)
            self.last_game_over_time = pygame.time.get_ticks()
            return 0
        else:
            return 1

    def open_github(self):
        url = "https://github.com/f4rys"
        webbrowser.open(url, new=0, autoraise=True)

    def handle_resize(self, w, h):
        # PAUSE GAME
        if self.current_screen == 1:
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
        self.game_font = pygame.font.Font(resource_path('font/pixeled.ttf'), (self.screen_size[0] + self.screen_size[1]) // 70)

        # RESIZE SCREEN
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

        # RESIZE PLAYER
        self.player.sprite.update_screen_size(self.screen_size)

        # RESIZE SCORE RECTS
        self.score_system.update_screen_size(self.screen_size)

        # RESIZE OBSTACLES
        for obstacle in self.obstacle_group:
            obstacle.update_screen_size(self.screen_size)

    def run(self):
        # GAME LOOP
        while True:
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
                        current_time = pygame.time.get_ticks()
                        if current_time - self.last_game_over_time > 500:
                            self.start_game()
                    # OPEN PAUSE MENU THROUGH ESC
                    if event.key == pygame.K_ESCAPE and self.current_screen == 1:
                        self.pause_game()
                    # RETURN FROM PAUSE MENU THROUGH ESC
                    elif event.key == pygame.K_ESCAPE and self.current_screen == 2:
                        self.resume_game()
                    # FULLSCREEN TOGGLE WITH F11
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

                # ADD NEW OBSTACLE
                if event.type == self.obstacle_timer and self.current_screen == 1 and pygame.time.get_ticks() - self.resize_time > 1000:
                    self.resize_time = 0
                    self.obstacle_group.add(Obstacle(choice(['stone1', 'stone1', 'stone2']), self.screen_size))

                # WHEN RESIZING WINDOW
                if event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event.w, event.h)

            # START / GAME OVER MENU
            if self.current_screen == 0:
                if self.score != 0:
                    self.game_over_screen.frame(self.screen_size, events, self.score, best_score)
                else:
                    self.start_game_screen.frame(self.screen_size, events, best_score)

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

                # DRAW [ESC] and [X] BUTTONS
                Button(self.screen_size[0] - self.screen_size[0] // 6, self.screen_size[1] // 14, self.game_font, "[ESC]", self.screen, self.pause_game, events).process()
                Button(self.screen_size[0] - self.screen_size[0] // 14, self.screen_size[1] // 14, self.game_font, "[X]", self.screen, self.quit_game, events, "Red").process()

            # PAUSE MENU
            elif self.current_screen == 2:
                self.pause_game_screen.frame(self.screen_size, events, best_score, self.settings)

            pygame.display.update()
            self.clock.tick(60)
