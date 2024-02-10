from cryptography.fernet import Fernet, InvalidToken
import pygame

class Mechanics():
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.score_rectangle = None
        self.score_surface = None

    def load_encryption_key(self):
        with open('.key', 'rb') as file:
            key = file.read()
        return key

    def load_best_score(self):
        try:
            key = self.load_encryption_key()
            with open('best_score.txt', 'rb') as file:
                encrypted_data = file.read()

            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)
            best_score = int(decrypted_data.decode())
        except (FileNotFoundError, ValueError, InvalidToken):
            best_score = 0
        return best_score

    def save_best_score(self, score):
        best_score = self.load_best_score()
        if score > best_score:
            key = self.load_encryption_key()
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(str(score).encode())

            with open('best_score.txt', 'wb') as file:
                file.write(encrypted_data)

    def display_score(self, game_font, start_time, screen):
        current_time = int(pygame.time.get_ticks()/1000) - start_time
        self.score_surface = game_font.render(str(current_time) + " s", False, 'White')
        self.score_rectangle = self.score_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 14))
        screen.blit(self.score_surface, self.score_rectangle)
        return current_time

    def collision_sprite(self, player, obstacle_group, game_over_sound, channel, score):
        # MASKS FOR PIXEL PERFECT COLLISION DETECTION
        if pygame.sprite.spritecollideany(player.sprite, obstacle_group, pygame.sprite.collide_mask):
            obstacle_group.empty()
            channel.play(game_over_sound)
            self.save_best_score(score)
            return 0
        else:
            return 1
        
    def update_screen_size(self, screen_size):
        self.screen_size = screen_size
        if(self.score_rectangle and self.score_surface):
            self.score_rectangle = self.score_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 14))

    def reset_best_score(self):
        # ERASE CONTENT FROM BEST SCORE FILE
        try:
            with open('best_score.txt', 'w') as file:
                file.truncate(0)
        except Exception as e:
            print(f"Error: {e}")