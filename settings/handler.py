import json
import os


last_kernel_key = 'last_metakernel'
last_repo_key = 'last_kernel_repo'
last_start_date = 'last_start_date'


class PersistenceSettings:

    file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'tmp',
        'settings.json'
    )

    def __init__(self) -> None:
        if not self.load():
            self.reset_settings()

    def get(self, mission, key, default=None):
        mission_settings = self.settings.get(mission)
        if mission_settings:
            return mission_settings.get(key, default)
        return default
    
    def set(self, mission, key, value):
        mission_settings = self.settings.get(mission)
        if mission_settings is None:
            self.settings[mission] = {}
            mission_settings = self.settings[mission]
        mission_settings[key] = value
        

    def reset_settings(self):
        self.settings = {}
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.save()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.settings = json.load(file)
            return True
        return False

    def save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.settings, file)
        return True

class RuntimeSettings:

    def __init__(self) -> None:
        self.settings = {}


    def load(self, filename):

        file_path = os.path.join(
            os.path.dirname(__file__),
            'data',
            filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.settings.update(json.load(file))
            return True
        return False

    def update(self, new_settings):
        self.settings.update(new_settings)

    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
