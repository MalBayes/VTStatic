import json
import aiofiles
import jsonschema

from debug_log import mdm_logger
from pathlib import Path
from pubsub import MessageBusRegistry


class ModelConfigManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.tmp_config_path = config_path.parent.joinpath(".tmp")
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
        # Corny bug mitigation part 2. Because of the reasons I don't really know, something (I think it is VTS)
        # during whole save config-reload model-load config replaces content of vtube.json file with some unexpected
        # values, when values loaded in VTS are actually correct. I'll have to ask about that on VTS Discord
        if self.tmp_config_path.exists():
            self.config_path.write_bytes(self.tmp_config_path.read_bytes())
            self.tmp_config_path.unlink()
        # Corny bug mitigation part 2 ends here. I promise to do that more self-containing in the next commits
        await self.load_config()
        await self.load_saved_settings_list()

    async def load_config(self):
        async with aiofiles.open(self.config_path, 'r') as config_file:
            all_model_settings_raw = await config_file.read()
            all_model_settings = json.loads(all_model_settings_raw)
            self.model_settings = all_model_settings['ParameterSettings']
            jsonschema.validate(self.model_settings, self.model_settings_schema)
        await self.send_settings_to_gui()
        mdm_logger.debug("")

    async def send_settings_to_gui(self):
        message_bus = MessageBusRegistry.get_message_bus("slider_list_updater")
        for setting_entry in self.model_settings:
            message_bus.publish(setting_entry)

    async def load_custom_settings(self):
        mdm_logger.debug("")
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
        mdm_logger.debug("")

    async def send_saved_settings_list_to_gui(self):
        message_bus = MessageBusRegistry.get_message_bus("saved_settings_list_updater")
        for saved_setting_name in self.saves_settings_list:
            message_bus.publish(saved_setting_name)

    def receive_selected_setting(self, message):
        self.selected_setting = message['text']

    async def save_parameter_settings(self, save_name):
        mdm_logger.debug("")
        custom_setting_path = self.custom_settings_path / save_name
        custom_setting_path.with_suffix(".json")
        if not self.custom_settings_path.exists():
            self.custom_settings_path.mkdir()
        with custom_setting_path.open(mode="w") as file:
            json.dump(self.model_settings, file, indent=4)
            await self.send_settings_to_gui()
            await self.load_saved_settings_list()
