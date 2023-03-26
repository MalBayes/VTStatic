# Testing script against VTube Studio API. Can introduce changes in VTS settings. User discretion is advised.
# Test cases assumes you have VTube Studio already running
import asyncio
import os
import shutil
import unittest
import threading
import socket
import json
from pathlib import Path
from unittest.mock import patch, PropertyMock

from kivy.app import App

import gui
import websocket_driver
from model_config_manager import ModelConfigManager
from vts_comm import VTSComm

run_long_tests = False
run_gui_tests = True
run_vts_tests = False

if __name__ == '__main__':
    unittest.main()


class BroadcastCheck(unittest.TestCase):
    def test_receive_message(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('0.0.0.0', 47779))

        def receive_message():
            nonlocal message_received
            data, address = sock.recvfrom(1024)
            if b"VTubeStudioAPIStateBroadcast" in data:
                message_received = True

        message_received = False
        thread = threading.Thread(target=receive_message)
        thread.start()
        thread.join(timeout=10)
        self.assertTrue(message_received)
        sock.close()


class WebSocketCheck(unittest.TestCase):
    async def connect_to_websocket(self):
        websocket_pool = websocket_driver.WebSocketPool()
        self.manager = websocket_pool.get_free_socket(url='ws://localhost:8001')
        message = json.loads('''
                        {
                            "apiName": "VTubeStudioPublicAPI",
                            "apiVersion": "1.0",
                            "requestID": "MyIDWithLessThan64Characters",
                            "messageType": "APIStateRequest"
                        }
                        ''')
        await self.manager.send(json.dumps(message))
        response = await self.manager.receive()
        self.assertIn('MyIDWithLessThan64Characters', response)
        await self.manager.close()

    def test_send_message(self):
        asyncio.run(self.connect_to_websocket())


class WebSocketCloseCheck(unittest.TestCase):
    async def websocket_wait_till_end(self):
        websocket_pool = websocket_driver.WebSocketPool()
        self.manager = websocket_pool.get_free_socket(url='ws://localhost:8001')
        message = json.loads('''
                        {
                            "apiName": "VTubeStudioPublicAPI",
                            "apiVersion": "1.0",
                            "requestID": "MyIDWithLessThan64Characters",
                            "messageType": "APIStateRequest"
                        }
                        ''')
        await self.manager.send(json.dumps(message))
        self.assertIsNotNone(self.manager.last_used)
        await asyncio.sleep(11)
        self.assertIsNone(self.manager.last_used)

    @unittest.skipUnless(run_long_tests, "Skipping WebSocketCloseCheck test")
    def test_websocket_timeout_close(self):
        asyncio.run(self.websocket_wait_till_end())


class ModelConfigurationLoad(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_resources")
        os.chdir(test_dir)
        shutil.copy(r".\akari_orig.vtube.json", r".\akari.vtube.json")

    async def load_model_configuration(self):
        model_configuration = ModelConfigManager(Path(r".\akari.vtube.json"))
        await model_configuration.initialize()
        await model_configuration.save_custom_settings("test_setting")

    def test_load_model_configuration(self):
        asyncio.run(self.load_model_configuration())


class WindowlessGuiOperations(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_resources")
        os.chdir(test_dir)
        shutil.copy(r".\akari_orig.vtube.json", r".\akari.vtube.json")
        logic = VTSComm()
        self.gui_instance = gui.MyApp(logic)
        self.built_gui = self.gui_instance.build()

    async def gui_load_model_configuration(self):
        model_configuration = ModelConfigManager(Path(r".\akari.vtube.json"))
        await model_configuration.initialize()
        await model_configuration.save_custom_settings("test_setting")

    def test_gui_load_model_configuration(self):
        asyncio.run(self.gui_load_model_configuration())


def mock_auth_button_press(self):
    print(self.model_config_manager)


class WindowGuiOperations(unittest.TestCase):
    def setUp(self):
        test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_resources")
        os.chdir(test_dir)
        shutil.copy(r".\akari_orig.vtube.json", r".\akari.vtube.json")

    def gui_load_model_configuration(self):
        logic = VTSComm()
        logic.model_config_manager = ModelConfigManager(Path(r".\akari.vtube.json"))

        def initialize_model_from_file_mock(*args, **kwargs):
            asyncio.create_task(logic.model_config_manager.initialize())
        def apply_and_reload_model_mock(*args, **kwargs):
            asyncio.create_task(logic.apply_settings())
            asyncio.create_task(logic.model_config_manager.initialize())

        with unittest.mock.patch.object(logic, 'initialize_model_from_file', side_effect=initialize_model_from_file_mock):
            with unittest.mock.patch.object(logic, 'apply_and_reload_model',
                                            side_effect=apply_and_reload_model_mock):
                gui_instance = gui.MyApp(logic)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    App.async_run(gui_instance, async_lib='asyncio'))
                loop.close()

    @unittest.skipUnless(run_gui_tests, "Skipping GUI test")
    def test_sanity_check(self):
        self.gui_load_model_configuration()
