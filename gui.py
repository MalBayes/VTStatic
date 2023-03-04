import asyncio

import kivy

from debug_log import gui_logger
from vts_comm import VTSComm

kivy.require('1.11.1')

from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class MySlider(BoxLayout):
    def __init__(self, value, min_value=0, max_value=100, **kwargs):
        super(MySlider, self).__init__(**kwargs)
        self.value = NumericProperty()
        self.slider = Slider(min=min_value, max=max_value, value=50, step=1)
        self.text_input = TextInput(multiline=False, text="50")

        self.value = value
        self.slider.bind(value=self.on_value)
        self.text_input.bind(on_text_validate=self.on_text_validate)

        self.add_widget(self.slider)
        self.add_widget(self.text_input)

    def on_value(self, instance, value):
        self.value = value
        self.text_input.text = str(value)

    def on_text_validate(self, text_input_handler: TextInput):
        try:
            self.value = float(text_input_handler.text)
            self.slider.value = self.value
        except ValueError:
            self.value = 0


class TitleSlider(BoxLayout):
    def __init__(self, text="Dummy", **kwargs):
        super(TitleSlider, self).__init__(orientation='vertical', **kwargs)
        self.label = Label(text=text)
        self.my_slider = MySlider(value=50)
        self.add_widget(self.label)
        self.add_widget(self.my_slider)


class SliderList(BoxLayout):
    def __init__(self, **kwargs):
        super(SliderList, self).__init__(orientation='vertical', **kwargs)


class SteeringPanel(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(SteeringPanel, self).__init__(**kwargs)
        self.auth_button = Button(text='authenticate')
        self.model_dir_button = Button(text='choose model directory')
        self.reload_model_button = Button(text='reload model')
        self.ids["auth_button"] = self.auth_button
        self.ids["model_dir_button"] = self.model_dir_button
        self.ids["reload_model_button"] = self.reload_model_button

        self.add_widget(self.auth_button)
        self.add_widget(self.model_dir_button)
        self.add_widget(self.reload_model_button)

        self.auth_button.bind(on_press=logic.on_auth_button_press)
        self.reload_model_button.bind(on_press=logic.on_model_reload_button_press)


class RootWidget(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.logic = logic
        self.slider_list = SliderList()
        self.steering_panel = SteeringPanel(self.logic)
        self.ids["slider_list"] = self.slider_list
        self.ids["steering_panel"] = self.steering_panel
        self.add_widget(self.slider_list)
        self.add_widget(self.steering_panel)



class MyApp(App):
    def __init__(self, logic, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.logic = logic

    def build(self):
        root_widget = RootWidget(self.logic)
        return root_widget


class MockLogic():
    def on_auth_button_press(self, instance):
        gui_logger.debug("button pressed")

    def on_model_reload_button_press(self, instance):
        gui_logger.debug("button pressed")

if __name__ == '__main__':
    mock_logic = MockLogic()
    gui_instance = MyApp(mock_logic)
    build_gui = gui_instance.build()
    gui_instance.run()
