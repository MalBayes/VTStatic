import json
import websocket_driver

token_request: json = json.loads('''
    {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "SomeID",
        "messageType": "AuthenticationTokenRequest",
        "data": {
            "pluginName": "My Cool Plugin",
            "pluginDeveloper": "My Name",
            "pluginIcon": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACl0lEQVR4nO3c0VLrMAxFUZf//+fwBMOEJo1tWUrO2ev91rdoWx0opTUAAAAAAODiteRRt7adnLjmTAyJG8bZ0I9PJ4Zi8wMYGfz//wUhFPma+tcRw498HHQbu3krB8Y2SNW/AVbfVrZBqrmXADxeXwBZt5MtkOZ6ANlDIYIUvASYuxZA1W1kCyzHBjBHAOY+B1C9hqvPF8cGMEcA5gjAHAGYIwBzBGDucwDV789Xny+ODWCOAMxdC6BqDbP+l2MDmLseQPZt5Pan6NsAWUNh+Gl4CTDXH8Dq28ntTzX3xY58r57Bl5h7CYgaGsMvw6eDzfH3AQAAAAAA8GH5PfnWjn9O8TL7mtg82bOhH3GIQf4Jjgx+TzkE6d8HiBh+5OPckWTZKwemtg3kNsDq26q2DeQCQB+pALJup9IWkAkgeygqEcgEgDESAVTdRoUtIBEAxhGAuccHUL2Gq8+f9fgAMIcAzBGAOQIwRwDmCMDc4wOofn+++vxZjw8AcwjAnEQAVWv46eu/NZEAME4mgOzbqHD7WxMKoLW8oagMvzWxANBPLoDVt1Pp9rcm9mT2It+rVxv8D7kN8FfU0FSH35rwE9vj08HvyT/Bd/j7AAAAAAAAU3zPe0vbyQ+tXqEzI4DbOBv6kfkYCKDcyOD3xkOQfjPo/iKGP/c4bIASUYN/p28bsAHSrRx+/+MTgDkCSLX69vefQwBpsobfdx4BmCOAFNm3//q5BGCOAMwRwHJV6//a+QRgjgDMEYA5AjBHAOYIwBwBLBf7O3zR5xOAOQIwRwApql4GPp9LAOYIIE32Frh2HgGkyorg+jkEYI4A0q3eAn2PzwdDSkX+rsBYWGyAUlHbYPxx2AC3waeD8Svv7wMAAAAAAKx8Ayb6crJm3XwXAAAAAElFTkSuQmCC"
        }
    }
''')


async def authenticate():
    web_socket = websocket_driver.websocket_pool.get_free_socket('ws://localhost:8001')
    await web_socket.send(json.dumps(token_request))
    response = await web_socket.receive()
    print(response)
