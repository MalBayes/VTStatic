import kivy
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from debug_log import gui_logger

kivy.require('1.11.1')

from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty
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


class ButtonsPanel(BoxLayout):
    def __init__(self, logic, **kwargs):
        super(ButtonsPanel, self).__init__(orientation='vertical', **kwargs)
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
        self.model_dir_button.bind(on_press=logic.on_model_dir_button_press)
        self.reload_model_button.bind(on_press=logic.on_model_reload_button_press)


Builder.load_string('''
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
''')


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
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.viewclass = 'SelectableLabel'
        self.data = [{'text': str(x)} for x in range(100)]

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

    def on_model_dir_button_press(self, instance):
        gui_logger.debug("button pressed")


if __name__ == '__main__':
    mock_logic = MockLogic()
    gui_instance = MyApp(mock_logic)
    build_gui = gui_instance.build()
    gui_instance.run()
