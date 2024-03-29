import asyncio
import os
import sys

from kivy.app import App
from kivy.resources import resource_add_path

import gui
from vts_comm import VTSComm

if __name__ == '__main__':
    logic = VTSComm()
    gui_instance = gui.MyApp(logic)
    loop = asyncio.get_event_loop()
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    loop.run_until_complete(
        App.async_run(gui_instance, async_lib='asyncio'))
    loop.close()
