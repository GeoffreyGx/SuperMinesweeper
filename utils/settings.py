import os

class Settings:
    def __init__(self) -> None:
        self.settings = {}

    def getSetting(self, settings_id):
        return self.settings[settings_id]

    def setSetting(self, setting_id: str, state: str):
        self.settings[setting_id] = state

    def saveSettingsToFile(self):
        with open("client.properties", "w") as settingsFile:
            str = ""
            for key, value in self.settings.items():
                str += f"${key}:${value}"
            settingsFile.write(str)
        