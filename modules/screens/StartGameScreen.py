import pygame

from modules.Button import Button

from resource_path import resource_path

class StartGameScreen():
    def __init__(self, screen, game_font, parent):
        self.parent = parent
        self.screen = screen
        self.game_font = game_font

        self.sky_surface = pygame.image.load(resource_path('images/sky.jpg')).convert()
        self.vignette_surface = pygame.image.load(resource_path('images/vignette.png')).convert_alpha()

    def frame(self, screen_size, events, best_score):
        self.screen.blit(pygame.transform.scale(self.sky_surface, screen_size), (0, 0))
        self.screen.blit(pygame.transform.scale(self.vignette_surface, screen_size), (0, 0))

        # RENDERS AND RECTANGLES
        best_score_message = self.game_font.render(f"BEST SCORE: {best_score}", False, "White")
        best_score_message_rect = best_score_message.get_rect(center=(screen_size[0] // 2, screen_size[1] // 1.1))

        # DRAW ELEMENTS
        self.screen.blit(best_score_message, best_score_message_rect)
        Button(screen_size[0] // 2, screen_size[1] // 1.25, self.game_font, "CLICK OR PRESS 'SPACE' TO START", self.screen, self.parent.start_game, events).process()
        Button(screen_size[0] // 2, screen_size[1] // 12, self.game_font, "[VISIT MY GITHUB]", self.screen, self.parent.open_github, events).process()
        Button(screen_size[0] - screen_size[0] // 14, screen_size[1] // 14, self.game_font, "[X]", self.screen, self.parent.quit_game, events, "Red").process()