import pygame

class Button():
    def __init__(self, x, y, font, text, screen, on_click_function, events, hover_colour="Gray"):
        self.events = events
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.screen = screen
        self.on_click_function = on_click_function
        self.hover_colour = hover_colour

        self.button_text = font.render(text, True, "White")
        self.button_rect = self.button_text.get_rect(center=(x,y))

    def process(self):
        mouse = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(mouse):
            self.button_text = self.font.render(self.text, True, self.hover_colour)
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click_function()

        self.screen.blit(self.button_text, self.button_rect)
