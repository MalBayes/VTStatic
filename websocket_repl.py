# REPL client to test requests on the go
import asyncio
import json
import websockets


async def repl_client():
    async with websockets.connect('ws://localhost:8001/') as websocket:
        while True:
            input_lines = []
            while True:
                line = input("> ")
                if not line:
                    break
                input_lines.append(line)
            data = '\n'.join(input_lines)
            if not data:
                continue
            if data.startswith('{'):
                message = json.loads(data)
            else:
                message = {'code': data}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(response)


if __name__ == "__main__":
    asyncio.run(repl_client())
