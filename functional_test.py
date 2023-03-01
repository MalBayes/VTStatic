# Testing script against VTube Studio API. Can introduce changes in VTS settings. User discretion is advised.
# Test cases assumes you have VTube Studio already running
import asyncio
import unittest
import threading
import socket
import json
from . import websocket_driver

run_long_tests = False

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