import os
import unittest

from modules.Settings import Settings

class TestSettings(unittest.TestCase):
    def setUp(self):
        try:
            os.remove(os.path.join(os.path.expanduser("~") + '/Marathoner', 'settings.ini'))
        except FileNotFoundError:
            pass

        self.settings = Settings()

    def test_default_settings(self):
        self.assertEqual(self.settings.music, 1)
        self.assertEqual(self.settings.sounds, 1)

    def test_update_settings(self):
        self.settings.update_settings(True, "Music")
        self.settings.update_settings(False, "Sounds")

        self.settings.config.read(self.settings.settings_file)
        self.assertEqual(self.settings.music, 1)
        self.assertEqual(self.settings.sounds, 0)
        self.assertEqual(self.settings.config.get("GENERAL", "Music"), "1")
        self.assertEqual(self.settings.config.get("GENERAL", "Sounds"), "0")

    def test_no_settings_file(self):
        os.remove(self.settings.settings_file)

        self.settings = Settings()
        self.assertEqual(self.settings.music, 1)
        self.assertEqual(self.settings.sounds, 1)
        self.assertTrue(os.path.exists(self.settings.settings_file))
