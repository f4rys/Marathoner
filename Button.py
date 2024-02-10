import pygame

class Button():
    def __init__(self, x, y, font, text, screen, on_click_function=None):
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.screen = screen
        self.on_click_function = on_click_function

        self.button_text = font.render(text, True, "White")
        self.button_rect = self.button_text.get_rect(center=(x,y))

    def process(self):
        mouse = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(mouse):
            self.button_text = self.font.render(self.text, True, "Gray")

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.on_click_function()

        self.screen.blit(self.button_text, self.button_rect)