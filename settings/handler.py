import json
import os


last_kernel_key = 'last_metakernel'
last_repo_key = 'last_kernel_repo'


class SettingsHandler:

    file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'tmp',
        'settings.json'
    )

    def __init__(self) -> None:
        if not self.load():
            self.reset_settings()

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
