import asyncio
import json
import websockets
from vts_commands import authenticate

if __name__ == '__main__':
    asyncio.run(authenticate())