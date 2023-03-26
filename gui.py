import random
import tkinter as tk
from tkinter import simpledialog

import kivy
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.widget import Widget

from debug_log import gui_logger
from pubsub import MessageBusRegistry

kivy.require('1.11.1')

from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.logger import Logger, LOG_LEVELS

Logger.setLevel(LOG_LEVELS["debug"])

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class CustomTextInput(TextInput):
    def __init__(self, text, multiline=False, slider=None):
        super(CustomTextInput, self).__init__(multiline=multiline, text=text, size_hint_x=0.3, size_hint_y=1.3)
        self.value = 0
        self.slider = slider
        self.bind(text=self.on_text)
        self.bind(on_text_validate=self.on_custom_text_validate)

    def on_text(self, instance, value):
        if hasattr(self, 'slider'):
            try:
                self.slider.value = float(value)
            except ValueError:
                pass

    def on_custom_text_validate(self, dummy):
        try:
            self.value = float(self.text)
            self.slider.value = self.value
        except ValueError:
            self.value = 0


class CustomSlider(Slider):
    def __init__(self, min_value, max_value, value=50):
        super(CustomSlider, self).__init__(value=value, min=min_value, max=max_value, step=0.1, sensitivity='handle')
        self.text_input = None
        self.bind(value=self.on_value)

    def on_value(self, instance, value):
        if hasattr(self, 'text_input'):
            instance.value = round(value, 1)
            self.text_input.text = str(instance.value)
            gui_logger.debug("Value changed for CustomSlider: {}".format(self))


class SettingSlider(BoxLayout):
    def __init__(self, min_value=-100, max_value=100, **kwargs):
        super(SettingSlider, self).__init__(**kwargs)
        self.slider = CustomSlider(min_value=min_value, max_value=max_value)
        self.text_input = CustomTextInput(multiline=False, text="50", slider=self.slider)
        self.slider.text_input = self.text_input
        self.add_widget(self.slider)
        self.add_widget(self.text_input)


class SettingSliderMirror(BoxLayout):
    def __init__(self, min_value=-100, max_value=100, **kwargs):
        super(SettingSliderMirror, self).__init__(**kwargs)
        self.slider = CustomSlider(min_value=min_value, max_value=max_value)
        self.text_input = CustomTextInput(multiline=False, text="50", slider=self.slider)
        self.slider.text_input = self.text_input
        self.add_widget(self.text_input)
        self.add_widget(self.slider)


class TitledSlider(BoxLayout):
    def __init__(self, text="Dummy", **kwargs):
        super(TitledSlider, self).__init__(orientation='vertical', **kwargs)
        self.text = text
        self.label = Label(text=self.text)
        self.my_slider = SettingSlider()
        self.add_widget(self.label)
        self.add_widget(self.my_slider)
        gui_logger.debug("Initialize TitledSlider: {}".format(self))


class TitledSliderMirror(BoxLayout):
    def __init__(self, text="Dummy", **kwargs):
        super(TitledSliderMirror, self).__init__(orientation='vertical', **kwargs)
        self.text = text
        self.label = Label(text=self.text)
        self.my_slider = SettingSliderMirror()
        self.add_widget(self.label)
        self.add_widget(self.my_slider)


class SettingSteer(RecycleDataViewBehavior, BoxLayout):
    index = None
    text = StringProperty()

    def __init__(self, **kwargs):
        super(SettingSteer, self).__init__(orientation='vertical', height=150, **kwargs)

        first_row = GridLayout(cols=2, rows=1)
        second_row = GridLayout(cols=2, rows=1)

        self.upper_left_ts = TitledSlider(text="Upper input boundary")
        first_row.add_widget(self.upper_left_ts)

        # self.upper_left_ts.my_slider.slider.value = self.dummy_value
        self.upper_right_ts = TitledSliderMirror(text="Upper output boundary")
        first_row.add_widget(self.upper_right_ts)

        self.lower_left_ts = TitledSlider(text="Lower input boundary")
        second_row.add_widget(self.lower_left_ts)
        self.lower_right_ts = TitledSliderMirror(text="Lower output boundary")
        second_row.add_widget(self.lower_right_ts)

        first_row.size_hint_y = 2
        self.add_widget(first_row)

        self.add_widget(Widget(size_hint_y=None, height=20))  # to move label a little bit lower
        self.title = Label(text=self.text, size_hint_y=1)
        self.add_widget(self.title)

        second_row.size_hint_y = 2
        self.add_widget(second_row)
        gui_logger.debug("Initialized SettingSteer: {}".format(self))

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = data['Name']
        # gui_logger.debug("SettingSteer index: {}, text: {}".format(self.index, self.text))
        self.title.text = self.text
        self.upper_left_ts.my_slider.slider.value = data.get('upper_left_value', 0)
        self.upper_right_ts.my_slider.slider.value = data.get('upper_right_value', 0)
        self.lower_left_ts.my_slider.slider.value = data.get('lower_left_value', 0)
        self.lower_right_ts.my_slider.slider.value = data.get('lower_right_value', 0)
        return super(SettingSteer, self).refresh_view_attrs(rv, index, data)

    def on_touch_up(self, touch):
        if super(SettingSteer, self).on_touch_down(touch):
            gui_logger.debug("on_touch_up executed")
            data_item = self.parent.parent.data[self.index]
            data_item['upper_left_value'] = self.upper_left_ts.my_slider.slider.value
            data_item['upper_right_value'] = self.upper_right_ts.my_slider.slider.value
            data_item['lower_left_value'] = self.lower_left_ts.my_slider.slider.value
            data_item['lower_right_value'] = self.lower_right_ts.my_slider.slider.value
            model_setting = self.parent.parent.logic.model_config_manager.model_settings[self.index]
            model_setting['InputRangeUpper'] = self.upper_left_ts.my_slider.slider.value
            model_setting['OutputRangeUpper'] = self.upper_right_ts.my_slider.slider.value
            model_setting['InputRangeLower'] = self.lower_left_ts.my_slider.slider.value
            model_setting['OutputRangeLower'] = self.lower_right_ts.my_slider.slider.value
            return True
        return False


config = '''
<SliderList>:
    viewclass: 'SettingSteer'
    SelectableRecycleBoxLayout:
        default_size: None, dp(150)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
        spacing: 50
'''


class SliderList(RecycleView):
    def __init__(self, logic, **kwargs):
        super(SliderList, self).__init__(always_overscroll=False, scroll_type=['bars'], bar_width='20px', **kwargs)
        self.message_bus = MessageBusRegistry.get_message_bus("slider_list_updater")
        self.titled_sliders = []
        self.message_bus.add_handler(self.add_slider)
        self.logic = logic

    def add_slider(self, message):
        gui_logger.debug("message: {}".format(message))
        slider_data = {
            'Name': message['Name'],
            'upper_left_value': message['InputRangeUpper'],
            'upper_right_value': message['OutputRangeUpper'],
            'lower_left_value': message['InputRangeLower'],
            'lower_right_value': message['OutputRangeLower']
        }
        self.data.append(slider_data)


config += '''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
'''
Builder.load_string(config)


# Define a custom layout class for a RecycleView widget
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    # This class adds selection and focus behavior to the RecycleView

    # Inherit from the FocusBehavior class to enable keyboard focus
    # Inherit from the LayoutSelectionBehavior class to enable selection of items
    # Inherit from the RecycleBoxLayout class, which is the default layout for the RecycleView
    pass


class SelectableLabel(RecycleDataViewBehavior, Label):
    """ Add selection support to the Label """
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    filename = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected
        if is_selected:
            rv.selected_setting = rv.data[index]
            rv.send_selected_label()
            gui_logger.debug("selection changed to {0}".format(rv.data[index]))
        else:
            gui_logger.debug("selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs, bar_width='20px')
        self.saved_settings_message_bus = MessageBusRegistry.get_message_bus("saved_settings_list_updater")
        self.saved_settings_message_bus.add_handler(self.add_saved_setting)
        self.selected_setting = ""
        self.selected_setting_message_bus = MessageBusRegistry.get_message_bus("selected_setting_updater")

    def add_saved_setting(self, message):
        gui_logger.debug("message: {}".format(message))
        saved_setting_data = {
            'text': message,
        }
        self.data.append(saved_setting_data)

    def send_selected_label(self):
        self.selected_setting_message_bus.publish(self.selected_setting)


class ButtonsPanel(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(ButtonsPanel, self).__init__(orientation='vertical', **kwargs)
        self.auth_button = Button(text='authenticate')
        self.model_dir_button = Button(text='choose model directory')
        self.reload_model_button = Button(text='reload model')
        self.save_settings = Button(text='save settings')
        self.load_settings = Button(text='load settings')
        self.logic = logic
        self.ids["auth_button"] = self.auth_button
        self.ids["model_dir_button"] = self.model_dir_button
        self.ids["reload_model_button"] = self.reload_model_button
        self.ids["save_settings"] = self.save_settings
        self.ids["load_settings"] = self.load_settings

        self.add_widget(self.auth_button)
        self.add_widget(self.model_dir_button)
        self.add_widget(self.reload_model_button)
        self.add_widget(self.save_settings)
        self.add_widget(self.load_settings)

        self.auth_button.bind(on_press=logic.on_auth_button_press)
        self.model_dir_button.bind(on_press=self.on_model_dir_button_press)
        self.reload_model_button.bind(on_press=self.on_reload_model_button_press)
        self.save_settings.bind(on_press=self.on_save_settings_button_press)
        self.load_settings.bind(on_press=self.on_load_settings_button_press)

    def clear_recycle_lists(self):
        gui_logger.debug("")
        for i in range(len(self.parent.parent.slider_list.data)):
            self.parent.parent.slider_list.data.pop(-1)
        for i in range(len(self.parent.my_widget.data)):
            self.parent.my_widget.data.pop(-1)

    def on_model_dir_button_press(self, instance):
        self.clear_recycle_lists()
        self.logic.initialize_model_from_file()

    def on_load_settings_button_press(self, instance):
        self.clear_recycle_lists()
        self.logic.load_selected_settings()

    def on_save_settings_button_press(self, instance):
        self.clear_recycle_lists()
        self.logic.save_current_settings()

    def on_reload_model_button_press(self, instance):
        self.clear_recycle_lists()
        self.logic.apply_and_reload_model()


class SteeringPanel(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(SteeringPanel, self).__init__(orientation='vertical', **kwargs)
        self.buttons_panel = ButtonsPanel(logic)
        self.add_widget(self.buttons_panel)
        self.my_widget = RV()
        self.add_widget(self.my_widget)


class RootWidget(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.logic = logic
        self.slider_list = SliderList(self.logic)
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
        message_bus = MessageBusRegistry.get_message_bus("slider_list_updater")
        message_bus.publish("herp")

    def on_model_reload_button_press(self, instance):
        gui_logger.debug("button pressed")

    def initialize_model_from_file(self, instance):
        gui_logger.debug("button pressed")

    def on_save_settings(self, instance):
        tk_root = tk.Tk()
        tk_root.withdraw()
        save_name = simpledialog.askstring(title="Test",
                                           prompt="What's your Name?:")


if __name__ == '__main__':
    mock_logic = MockLogic()
    gui_instance = MyApp(mock_logic)
    gui_instance.run()
