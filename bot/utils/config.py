import json
from pathlib import Path


class ConfigUtil:
    def __init__(self, config_location = "./config/persistent.json"):
        self.loc = Path(config_location)
        self.data = None

        if not self.loc.exists():
            with self.loc.open('w') as f:
                json.dump({}, f)

        with self.loc.open() as f:
            self.data = json.load(f)

    def read(self):
        return self.data

    def write(self):
        with self.loc.open('w') as f:
            json.dump(self.data, f)

    def get_attr(self, name: str):
        if name in self.data:
            return name
        return None

    def set_attr(self, name: str, value):
        self.data[name] = value
        self.write()

    def has_attr(self, name: str):
        return name in self.data
