import json
from pathlib import Path

import jsonschema

from pubsub import MessageBusRegistry


class ModelConfigManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.custom_settings_path: Path = Path(r".\vtstatic_conf")
        self.model_settings: dict = {}
        self.model_settings_schema = {
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
        self.current_settings_name_tmp: str = ""
        self.saves_settings_list: list = []
        self.selected_setting_message_bus = MessageBusRegistry.get_message_bus("selected_setting_updater")
        self.selected_setting = ""
        self.selected_setting_message_bus.add_handler(self.receive_selected_setting)

    async def initialize(self):
        await self.load_config()
        await self.load_saved_settings_list()

    async def load_config(self):
        with self.config_path.open(mode="r") as file:
            all_model_settings = json.load(file)
            self.model_settings = all_model_settings['ParameterSettings']
            jsonschema.validate(self.model_settings, self.model_settings_schema)
        await self.send_settings_to_gui()

    async def send_settings_to_gui(self):
        message_bus = MessageBusRegistry.get_message_bus("slider_list_updater")
        for setting_entry in self.model_settings:
            message_bus.publish(setting_entry)

    async def save_custom_settings(self, custom_settings_name: str):
        custom_setting_path = self.custom_settings_path / custom_settings_name
        custom_setting_path.with_suffix(".json")
        if not self.custom_settings_path.exists():
            self.custom_settings_path.mkdir()
        with custom_setting_path.open(mode="w") as file:
            file.write(json.dumps(self.model_settings, indent=4))

    async def load_custom_settings(self):
        custom_setting_path = self.custom_settings_path / self.selected_setting
        custom_setting_path.with_suffix(".json")
        with custom_setting_path.open(mode="r") as file:
            self.model_settings = json.load(file)
            await self.send_settings_to_gui()
            await self.load_saved_settings_list()

    async def load_saved_settings_list(self):
        model_path = self.config_path.parent / self.custom_settings_path
        if not model_path.exists():
            return
        file_list = [file.name for file in self.custom_settings_path.glob('*') if file.is_file()]
        self.saves_settings_list = file_list
        await self.send_saved_settings_list_to_gui()

    async def send_saved_settings_list_to_gui(self):
        message_bus = MessageBusRegistry.get_message_bus("saved_settings_list_updater")
        for saved_setting_name in self.saves_settings_list:
            message_bus.publish(saved_setting_name)

    def receive_selected_setting(self, message):
        self.selected_setting = message['text']

    async def save_parameter_settings(self, save_name):
        custom_setting_path = self.custom_settings_path / save_name
        custom_setting_path.with_suffix(".json")
        with custom_setting_path.open(mode="w") as file:
            json.dump(self.model_settings, file, indent=4)
            await self.send_settings_to_gui()
            await self.load_saved_settings_list()
