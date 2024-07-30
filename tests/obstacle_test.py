import unittest
import pygame

from modules.Obstacle import Obstacle

class TestObstacle(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size, pygame.RESIZABLE)

    def tearDown(self):
        pygame.quit()

    def test_load_stone1_type_obstacle(self):
        obstacle = Obstacle('stone1', self.screen_size)

        self.assertIsNotNone(obstacle.image)

        expected_y_pos = self.screen_size[1] * 0.74
        self.assertEqual(obstacle.rect.midbottom[1], expected_y_pos)

    def test_load_stone2_type_obstacle(self):
        obstacle = Obstacle('stone2', self.screen_size)

        self.assertIsNotNone(obstacle.image)

        expected_y_pos = self.screen_size[1] * 0.49
        self.assertEqual(obstacle.rect.midbottom[1], expected_y_pos)

    def test_update_changes_rect_x(self):
        obstacle = Obstacle('stone1', self.screen_size)
        original_x = obstacle.rect.x

        obstacle.update()

        self.assertEqual(obstacle.rect.x, original_x - 10)

    def test_destroy_kills_obstacle(self):
        obstacle = Obstacle('stone1', self.screen_size)
        obstacle.rect.x = -(self.screen_size[0] + 50)

        obstacle.destroy()

        self.assertFalse(obstacle.alive())

    def test_update_screen_size_changes_image_and_rect(self):
        obstacle = Obstacle('stone1', self.screen_size)

        original_image = obstacle.image
        original_rect = obstacle.rect

        new_screen_size = (1000, 500)
        obstacle.update_screen_size(new_screen_size)

        self.assertIsNot(original_image, obstacle.image)
        self.assertIsNot(original_rect, obstacle.rect)
