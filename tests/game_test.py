import unittest
from unittest.mock import MagicMock

import pygame

from modules.Game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.game = Game()

    def tearDown(self):
        pygame.quit()

    def test_toggle_fullscreen(self):
        original_screen_size = self.game.screen_size

        self.game.toggle_fullscreen()
        self.assertTrue(self.game.fullscreen)
        self.assertEqual(self.game.screen_size, tuple(self.game.monitor_size))

        self.game.toggle_fullscreen()
        self.assertFalse(self.game.fullscreen)
        self.assertEqual(self.game.screen_size, original_screen_size)

    def test_toggle_music(self):
        self.game.channel1 = MagicMock()

        self.game.toggle_music()
        self.game.channel1.pause.assert_called_once()
        self.assertTrue(self.game.music_muted)

        self.game.toggle_music()
        self.game.channel1.unpause.assert_called_once()
        self.assertFalse(self.game.music_muted)

    def test_toggle_sounds(self):
        self.game.channel2 = MagicMock()

        self.game.toggle_sounds()
        self.assertTrue(self.game.sounds_muted)

        self.game.toggle_sounds()
        self.assertFalse(self.game.sounds_muted)

    def test_start_game(self):
        self.game.start_game()
        self.assertEqual(self.game.current_screen, 1)

    def test_pause_game(self):
        self.game.pause_game()
        self.assertEqual(self.game.current_screen, 2)
        self.assertNotEqual(self.game.pause_time, 0)

    def test_resume_game(self):
        self.game.pause_game()
        pause_time = self.game.pause_time
        self.game.resume_game()
        self.assertEqual(self.game.current_screen, 1)
        self.assertEqual(self.game.pause_time, 0)
        self.assertEqual(self.game.start_time, self.game.start_time + int(pause_time / 1000))

    def test_collision_with_obstacle_group(self):
        pygame.sprite.spritecollideany = lambda sprite, group, collide_mask: True
        result = self.game.collision_sprite()
        self.assertEqual(result, 0)

    def test_no_collision_with_obstacle_group(self):
        pygame.sprite.spritecollideany = lambda sprite, group, collide_mask: False
        result = self.game.collision_sprite()
        self.assertEqual(result, 1)

    def test_handle_resize(self):
        original_screen_size = self.game.screen_size

        new_width = int(original_screen_size[0] * 1.5)
        self.game.handle_resize(new_width, original_screen_size[1])
        self.assertEqual(self.game.screen_size[0], new_width)
        self.assertEqual(self.game.screen_size[1], int(new_width / self.game.aspect_ratio))

        new_aspect_ratio = 2.0
        new_height = int(original_screen_size[1] / new_aspect_ratio)
        self.game.handle_resize(original_screen_size[0], new_height)
        self.assertEqual(self.game.screen_size[0], original_screen_size[0])
        self.assertEqual(self.game.screen_size[1], original_screen_size[1])
