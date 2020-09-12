import requests
import json

from datetime import datetime
from termcolor import colored

from config.config import hook

levels = {
    "debug": 5,
    "info": 4,
    "warn": 3,
    "error": 2,
    "critical": 1
}

colours = {
    "debug": 0xFFFFFF,
    "info": 0x00FF00,
    "warn": 0xFFFF00,
    "error": 0xA16F00,
    "critical": 0xFF0000
}

termc = {
    "debug": 'white',
    "info": 'green',
    "warn": 'yellow',
    "error": 'red',
    "critical": 'red'
}


class Logger:
    def __init__(self, logger_name, log_level="info", mode="embed"):
        self.name = logger_name
        self.level = levels[log_level]
        self.mode = mode

    def _send(self, data):
        requests.post(hook, data=json.dumps(data), headers={"Content-Type":"application/json"})

    def embed(self, logtype: str, content: str, colour: int):
        data = {}
        data["username"] = self.name
        data["avatar_url"] = "https://vcokltfre.github.io/service.png"
        data["embeds"] = [{
            "title": logtype,
            "description": content,
            "footer": {"text": f"Made by vcokltfre#6868 | {datetime.now()}"},
            "color": colour
        }]
        self._send(data)

    def message(self, logtype: str, content: str):
        timestamp = str(datetime.now()).split(".")[0]
        content = f"__**{logtype}**__ @ {timestamp}:\n{content}"
        data = {
            "username": self.name,
            "content": content.replace("@", "@​") # Zero width space to remove mentions
        }
        self._send(data)

    def send(self, logtype: str, content: str):
        if levels[logtype] <= self.level:
            logtype = logtype.upper()
            if self.mode == "embed":
                colour = colours[logtype.lower()]
                self.embed(logtype, content, colour)
            else:
                self.message(logtype, content)

            content = content.split('\n')[0]
            print(colored(f"[{logtype}] {content}", termc[logtype.lower()]))

    def debug(self, content):
        self.send("debug", content)

    def info(self, content):
        self.send("info", content)

    def warn(self, content):
        self.send("warn", content)

    def error(self, content):
        self.send("error", content)

    def critical(self, content):
        self.send("critical", content)