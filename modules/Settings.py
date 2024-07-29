import os
import configparser

class Settings():
    def __init__(self):
        self.settings_file = os.path.join(os.path.expanduser("~") + '/Marathoner', 'settings.ini')
        self.config = configparser.ConfigParser()

        self.music = 1
        self.sounds = 1

        if not os.path.exists(self.settings_file):
            default_settings = {
            'GENERAL': {
                'Music': 1,
                'Sounds': 1
                }
            }

            for section, settings in default_settings.items():
                self.config.add_section(section)
                for key, value in settings.items():
                    self.config.set(section, key, str(value))

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        else:
            self.config.read(self.settings_file)
            self.music = int(self.config.get("GENERAL", "Music"))
            self.sounds = int(self.config.get("GENERAL", "Sounds"))

    def update_settings(self, state, setting):
        if state:
            self.config.set("GENERAL", setting, "1")
        else:
            self.config.set("GENERAL", setting, "0")

        if setting == "Music":
            self.music = int(state)
        elif setting == "Sounds":
            self.sounds = int(state)

        with open(self.settings_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
