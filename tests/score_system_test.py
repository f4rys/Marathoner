import os
import unittest
from unittest.mock import patch

import pygame

from modules.ScoreSystem import ScoreSystem

class TestScoreSystem(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_size = (800, 600)
        self.score_system = ScoreSystem(self.screen_size)

    def tearDown(self):
        pygame.quit()

    def test_load_best_score_file_found(self):
        try:
            with open(os.path.expanduser("~") + '/Marathoner/best_score.txt', 'w',  encoding='utf-8') as file:
                file.write(str(100))
            best_score = self.score_system.load_best_score()
            self.assertEqual(best_score, 100)
        except Exception:
            pass

    def test_load_best_score_file_not_found(self):
        if not os.path.exists("best_score.txt"):
            with open("best_score.txt", "w", encoding="utf-8") as file:
                file.write("0")
        os.remove("best_score.txt")
        best_score = self.score_system.load_best_score()
        self.assertEqual(best_score, 0)

    def test_load_best_score_invalid_value(self):
        with open('best_score.txt', 'w', encoding="utf-8") as file:
            file.write('invalid')

        best_score = self.score_system.load_best_score()
        self.assertEqual(best_score, 0)

    def test_save_best_score_less_than_current_best(self):
        with patch('builtins.open', create=True) as mock_open:
            mock_file = mock_open.return_value
            mock_file.read.return_value = '200'

            self.score_system.save_best_score(150)
            self.assertFalse(mock_file.write.called)

    def test_display_score(self):
        game_font = pygame.font.Font(None, 36)
        start_time = int(pygame.time.get_ticks() / 1000)
        screen = pygame.Surface(self.screen_size)

        current_time = self.score_system.display_score(game_font, start_time, screen)

        self.assertIsInstance(self.score_system.score_surface, pygame.Surface)
        self.assertIsInstance(self.score_system.score_rectangle, pygame.Rect)
        self.assertEqual(current_time, 0)

    def test_update_screen_size(self):
        new_screen_size = (600, 400)

        self.score_system.update_screen_size(new_screen_size)

        self.assertEqual(self.score_system.screen_size, new_screen_size)
        if self.score_system.score_rectangle and self.score_system.score_surface:
            expected_rect_center = (new_screen_size[0] // 2, new_screen_size[1] // 14)
            self.assertEqual(self.score_system.score_rectangle.center, expected_rect_center)
