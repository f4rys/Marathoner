from cryptography.fernet import Fernet
import pygame

class Mechanics():
    def __init__(self):
        pass

    def load_encryption_key(self):
        with open('key.key', 'rb') as file:
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
        except (FileNotFoundError, ValueError):
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
        score_surface = game_font.render(str(current_time) + " s", False, 'White')
        score_rectangle = score_surface.get_rect(center=(640, 50))
        screen.blit(score_surface, score_rectangle)
        return current_time

    def collision_sprite(self, player, obstacle_group, game_over_sound, score):
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            obstacle_group.empty()
            game_over_sound.play()
            self.save_best_score(score)
            return False
        else:
            return True