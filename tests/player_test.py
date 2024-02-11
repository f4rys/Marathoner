import pygame
import unittest
from modules.Player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)
        self.player = Player(self.screen_size)

    def tearDown(self):
        pygame.quit()

    def test_load(self):
        self.assertGreater(len(self.player.player_run), 0)
        self.assertGreater(len(self.player.player_jump), 0)

        for img in self.player.player_run:
            self.assertIsInstance(img, pygame.Surface)
        for img in self.player.player_jump:
            self.assertIsInstance(img, pygame.Surface)

        initial_x = self.screen_size[0] // 10
        initial_y = self.screen_size[1] - self.screen_size[1] // 2

        self.assertEqual(self.player.rect.midbottom[0], initial_x)
        self.assertEqual(self.player.rect.midbottom[1], initial_y)

    def test_apply_gravity(self):
        self.player.gravity = 10
        initial_y = self.player.rect.y

        self.player.apply_gravity()

        self.assertEqual(self.player.gravity, 11)
        self.assertEqual(self.player.rect.y, initial_y + 11)

    def test_animation_state(self):
        self.player.jump_index = 0
        self.player.run_index = 0
        self.player.rect.bottom = self.screen_size[1] - self.screen_size[1] // 3.5 - 10
        self.player.animation_state()

        self.assertEqual(self.player.jump_index, 0.1)
        self.assertEqual(self.player.image, self.player.player_jump[0])

        self.player.rect.bottom = self.screen_size[1] - self.screen_size[1] // 3.5 + 10
        self.player.animation_state()

        self.assertEqual(self.player.run_index, 0.1)
        self.assertEqual(self.player.image, self.player.player_run[0])

    def test_update_screen_size(self):
        initial_screen_size = self.screen_size

        new_screen_size = (1024, 768)
        self.player.update_screen_size(new_screen_size)

        self.assertEqual(self.player.screen_size, new_screen_size)
        self.assertNotEqual(self.player.player_run, initial_screen_size)
        self.assertNotEqual(self.player.player_jump, initial_screen_size)
