import asyncio
import json
import os.path
import string
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog

from plyer import filechooser

import websocket_driver
from debug_log import comm_logger
from model_config_manager import ModelConfigManager
from vts_requests import gen_auth_token_request, gen_loaded_model_stats_request, gen_reload_current_model_request, \
    gen_auth_request


class VTSComm:
    def __init__(self):
        self.auth_token: string = ""
        self.curr_model_id: string = ""
        self.model_config_manager: ModelConfigManager = ModelConfigManager(Path(""))

    async def get_authentication_token(self):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_auth_token_request()))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        if "data" in response_dict:
            data_dict = response_dict["data"]
            if "authenticationToken" in data_dict:
                self.auth_token = response_dict["data"]["authenticationToken"]
                with open("auth.token", "w") as file:
                    file.write(self.auth_token)
            elif "errorID" in data_dict:
                comm_logger.error("Error ID: {}, message: {}".format(data_dict["errorID"], data_dict["message"]))

    async def authenticate(self, auth_token: string):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_auth_request(auth_token)))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        if "data" in response_dict:
            data_dict = response_dict["data"]
            if "authenticated" in data_dict:
                comm_logger.debug(
                    "authenticated: {}, reason: {}".format(data_dict["authenticated"], data_dict["reason"]))

    async def fresh_auth(self):
        auth_token_coro = asyncio.create_task(self.get_authentication_token())
        await auth_token_coro
        asyncio.create_task(self.authenticate(self.auth_token))

    def on_auth_button_press(self, instance):
        if os.path.exists("auth.token"):
            with open("auth.token", "r") as file:
                self.auth_token = file.read()
                asyncio.create_task(self.authenticate(self.auth_token))
        else:
            asyncio.create_task(self.fresh_auth())

    # def on_model_reload_button_press(self, instance):
    #     asyncio.create_task(self.apply_and_reload_model())

    async def apply_settings(self):
        with open(self.model_config_manager.config_path, 'r') as config_file:
            config_file_data = json.load(config_file)
        config_file_data["ParameterSettings"] = self.model_config_manager.model_settings
        with open(self.model_config_manager.config_path, 'w') as config_file:
            json.dump(config_file_data, config_file, indent=4)

    def apply_and_reload_model(self):
        asyncio.create_task(self.apply_settings())
        asyncio.create_task(self.load_model(self.curr_model_id))
        asyncio.create_task(self.model_config_manager.initialize())

    # async def get_loaded_model_stats(self):
    #     web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
    #     await web_socket.send(json.dumps(gen_loaded_model_stats_request()))
    #     response = await web_socket.receive()
    #     response_dict = json.loads(response)
    #     if "data" in response_dict:
    #         data_dict = response_dict["data"]
    #         if "errorID" in data_dict:
    #             comm_logger.error("Error ID: {}, message: {}".format(data_dict["errorID"], data_dict["message"]))
    #         elif "modelID" in data_dict:
    #             comm_logger.debug(
    #                 "modelLoaded: {}, modelName {}".format(data_dict["modelLoaded"], data_dict["modelName"]))
    #             self.curr_model_id = response_dict["data"]["modelID"]

    async def load_model(self, model_id):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_reload_current_model_request(model_id)))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        self.curr_model_id = response_dict["data"]["modelID"]

    # VTube Studio\VTube Studio_Data\StreamingAssets\Live2DModels
    # TODO: Move it to model_config_manager.py, it doesn't fit here, for now just send path through pubsub
    def initialize_model_from_file(self):
        model_json_config_path_tmp: str = filechooser.open_file(title="Pick model json config file (.json.vtube "
                                                                      "extention)...",
                                                                filters=[("Model config file", "*.vtube.json")])
        self.model_config_manager = ModelConfigManager(Path(model_json_config_path_tmp[0]))
        comm_logger.debug("Chosen config file: {}".format(self.model_config_manager.config_path))
        asyncio.create_task(self.model_config_manager.initialize())

    async def load_parameter_settings(self):
        pass

    def load_selected_settings(self):
        asyncio.create_task(self.model_config_manager.load_custom_settings())

    def save_current_settings(self):
        tk_root = tk.Tk()
        tk_root.withdraw()
        save_name = simpledialog.askstring(title="Save setting",
                                           prompt="Please provide a filename for the configuration setting")
        asyncio.create_task(self.model_config_manager.save_parameter_settings(save_name))
