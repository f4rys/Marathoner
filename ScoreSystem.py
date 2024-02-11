import pygame

class ScoreSystem():
    def __init__(self, screen_size):
        self.screen_size = screen_size

    def load_best_score(self):
        try:
            with open('best_score.txt', 'r') as file:
                best_score = int(file.read())
                return best_score
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0
        
    def save_best_score(self, score):
        best_score = self.load_best_score()
        if score > best_score:
            try:
                with open('best_score.txt', 'w') as file:
                    file.write(str(score))
            except Exception as e:
                print(f"Error while saving best score: {e}")

    def display_score(self, game_font, start_time, screen):
        current_time = int(pygame.time.get_ticks()/1000) - start_time
        self.score_surface = game_font.render(str(current_time) + " s", False, 'White')
        self.score_rectangle = self.score_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 14))
        screen.blit(self.score_surface, self.score_rectangle)
        return current_time
        
    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        if(self.score_rectangle and self.score_surface):
            self.score_rectangle = self.score_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 14))

    def reset_best_score(self):
        try:
            with open('best_score.txt', 'w') as file:
                file.write('0')
        except IOError as e:
            print(f"Error: {e}")