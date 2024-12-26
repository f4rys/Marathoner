import pygame

from modules.Button import Button

from resource_path import resource_path

class PauseGameScreen():
    def __init__(self, screen, game_font, parent):
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

        self.blur_surface = pygame.image.load(resource_path('images/blur.jpg')).convert_alpha()

    def frame(self, screen_size, events, best_score, settings):
        # DRAW BACKGROUND
        self.screen.blit(pygame.transform.scale(self.blur_surface, screen_size), (0, 0))

        # RENDERS
        music_message = "[UNMUTE MUSIC]" if not settings.music else "[MUTE MUSIC]"
        sounds_message = "[UNMUTE SOUND]" if not settings.sounds else "[MUTE SOUND]"

        pause_text = self.game_font.render("GAME PAUSED", False, "White")
        best_score_text = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")

        # RECTANGLES
        pause_text_rect = pause_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 4))
        best_score_text_rect = best_score_text.get_rect(center=(screen_size[0] // 2, screen_size[1] // 3))

        # DRAW ELEMENTS
        self.screen.blit(pause_text, pause_text_rect)
        self.screen.blit(best_score_text, best_score_text_rect)

        # BUTTONS LIST
        button_y = screen_size[1] // 2
        button_spacing = screen_size[1] // 12

        Button(screen_size[0] // 2, button_y, self.game_font, "[ABORT GAME]", self.screen, self.parent.abort_game, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing, self.game_font, "[FULLSCREEN F11]", self.screen, self.parent.toggle_fullscreen, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing * 2, self.game_font, "[RESET BEST SCORE]", self.screen, self.parent.score_system.reset_best_score, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing * 3, self.game_font, music_message, self.screen, self.parent.toggle_music, events).process()
        Button(screen_size[0] // 2, button_y + button_spacing * 4, self.game_font, sounds_message, self.screen, self.parent.toggle_sounds, events).process()

        # DRAW [ESC] and [X] BUTTONS
        Button(screen_size[0] - screen_size[0] // 6, screen_size[1] // 14, self.game_font, "[ESC]", self.screen, self.parent.resume_game, events).process()
        Button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, self.game_font, "[X]", self.screen, self.parent.quit_game, events, "Red").process()
