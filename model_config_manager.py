import json
from pathlib import Path

import jsonschema


class ModelConfigManager:
    config_path: Path = Path()
    custom_settings_path: Path = Path(r".\vtstatic_conf")
    model_settings: dict = {}
    model_settings_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "InputRangeLower": {"type": "number"},
                "InputRangeUpper": {"type": "number"},
                "OutputRangeLower": {"type": "number"},
                "OutputRangeUpper": {"type": "number"},
            },
            "required": ["InputRangeLower", "InputRangeUpper", "OutputRangeLower", "OutputRangeUpper"]
        },
        "minItems": 1,
    }
    current_settings_name: str = ""

    def __init__(self, config_path: Path):
        self.config_path = config_path

    async def initialize(self):
        await self.load_config()

    async def load_config(self):
        with self.config_path.open(mode="r") as file:
            all_model_settings = json.load(file)
            self.model_settings = all_model_settings['ParameterSettings']
            jsonschema.validate(self.model_settings, self.model_settings_schema)

    async def save_custom_settings(self, custom_settings_name: str):
        self.custom_settings_path = Path(custom_settings_name)
        custom_setting_path = self.custom_settings_path / custom_settings_name / ".json"
        if not self.custom_settings_path.exists():
            self.custom_settings_path.mkdir()
        with custom_setting_path.open(mode="w") as file:
            file.write(json.dumps(self.model_settings, indent=4))

    async def load_custom_settings(self, custom_settings_name: str):
        self.custom_settings_path = Path(custom_settings_name)
        custom_setting_path = self.custom_settings_path / custom_settings_name / ".json"
        with custom_setting_path.open(mode="r") as file:
            self.model_settings = json.load(file)
