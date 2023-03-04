import asyncio
import json
import os.path
import string
import websocket_driver
from vts_requests import gen_token_request, gen_loaded_model_stats_request, gen_reload_current_model_request


class VTSComm():
    def __init__(self):
        self.auth_token: string = ""
        self.curr_model_id: string = ""

    async def authenticate(self, auth_token=None):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_token_request(auth_token)))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        self.auth_token = response_dict["data"]["authenticationToken"]
        with open("auth.token", "w") as file:
            file.write(self.auth_token)

    def on_auth_button_press(self, instance):
        if os.path.exists("auth.token"):
            with open("auth.token", "r") as file:
                self.auth_token = file.read()
                asyncio.create_task(self.authenticate(auth_token=self.auth_token))
        else:
            asyncio.create_task(self.authenticate())

    def on_model_reload_button_press(self, instance):
        asyncio.create_task(self.reload_model())

    async def reload_model(self):
        get_stats_task = asyncio.create_task(self.get_loaded_model_stats())
        await get_stats_task
        asyncio.create_task(self.load_model(self.curr_model_id))

    async def get_loaded_model_stats(self):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_loaded_model_stats_request()))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        self.curr_model_id = response_dict["data"]["modelID"]

    async def load_model(self, model_id):
        web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
        await web_socket.send(json.dumps(gen_reload_current_model_request(model_id)))
        response = await web_socket.receive()
        response_dict = json.loads(response)
        self.curr_model_id = response_dict["data"]["modelID"]
