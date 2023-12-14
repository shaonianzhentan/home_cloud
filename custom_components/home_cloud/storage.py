import os
from homeassistant.helpers.storage import STORAGE_DIR
from homeassistant.util.json import load_json, save_json

class Storage():

    def __init__(self, filename) -> None:
        self.filename = self.get_storage_dir(filename)

    def get_storage_dir(self, file_name):
        return os.path.abspath(f'{STORAGE_DIR}/{file_name}')

    def load(self, default=None):
        if os.path.exists(self.filename):
            return load_json(self.filename)
        else:
            return default

    def save(self, data):
        save_json(self.filename, data)