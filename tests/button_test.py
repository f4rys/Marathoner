import unittest
import pygame
from unittest.mock import MagicMock
from Button import Button

class TestButton(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = MagicMock()
        self.font = pygame.font.Font('font/pixeled.ttf', 40)
        self.on_click_function = MagicMock()
        self.events = [MagicMock()]
        self.button = Button(100, 100, self.font, "Click me", self.screen, self.on_click_function, self.events)

    def tearDown(self):
        pygame.quit()

    def test_button_process_no_event(self):
        pygame.mouse.get_pos = MagicMock(return_value=(100, 100))
        self.button.process()

        self.assertEqual(repr(self.button.button_text), repr(self.font.render("Click me", True, "Gray")))
        self.on_click_function.assert_not_called()

    def test_button_process_with_event(self):
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.pos = (100, 100)
        self.events.append(event)
        pygame.mouse.get_pos = MagicMock(return_value=(100, 100))
        self.button.process()

        self.assertEqual(repr(self.button.button_text), repr(self.font.render("Click me", True, "Gray")))
        self.on_click_function.assert_called_once()