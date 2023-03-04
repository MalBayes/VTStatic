import asyncio
from kivy.clock import Clock
import gui
from functools import partial
from vts_commands import authenticate
from kivy.app import App


if __name__ == '__main__':
    gui_instance = gui.MyApp()
    built_gui = gui.MyApp().build()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        App.async_run(gui_instance, async_lib='asyncio'))
    loop.close()
