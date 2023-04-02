import asyncio
import time
from typing import List
import websockets

import config


class WebSocketManager:
    def __init__(self, url):
        self.url = url
        self.websocket = None
        self.last_used = None
        self.lock = asyncio.Lock()
        if config.debug_mode is False:
            self.timeout = 10
        else:
            self.timeout = 999999
        self.loop = asyncio.get_event_loop()
        self.monitor_task = self.loop.create_task(self.run())

    async def connect(self):
        self.websocket = await asyncio.wait_for(websockets.connect(self.url), 3)
        self.last_used = time.monotonic()

    async def close(self):
        await self.websocket.close()
        self.websocket = None
        self.last_used = None

    async def send(self, message):
        if self.websocket is None:
            await self.connect()
        else:
            self.last_used = time.monotonic()
        async with self.lock:
            try:
                await self.websocket.send(message)
            except:
                await self.close()

    async def receive(self):
        if self.websocket is None:
            await self.connect()
        else:
            self.last_used = time.monotonic()
        async with self.lock:
            try:
                result = await self.websocket.recv()
            except:
                await self.close()
            return result

    async def keep_alive(self):
        while True:
            if self.websocket is not None and time.monotonic() - self.last_used > self.timeout:
                await self.close()
            await asyncio.sleep(1)

    async def run(self):
        await asyncio.gather(self.keep_alive())


class WebSocketPool:
    def __init__(self):
        self.web_sockets: List[WebSocketManager] = []

    # Return free websocket for particular URL or creates new if not available
    def get_free_socket(self, url):
        for web_socket in self.web_sockets:
            if not web_socket.lock.locked():
                if web_socket.url == url:
                    return web_socket
        new_socket = WebSocketManager(url)
        self.web_sockets.append(new_socket)
        return new_socket


websocket_pool = WebSocketPool()
