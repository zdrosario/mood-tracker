# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

# PROJECT IMPORTS
import data.config as config

class CalViewToggleSet():
    buttons = {}
    src_selected = 'assets/selected.png'
    src_unselected = 'assets/unselected.png'

    def __init__(self):
        mood_cats = config.mood_data.get_weights()
        for mood in mood_cats:
            self.add_toggle(mood)
        self.add_toggle('overall')

        cur_view = self.get_visible()
        self.buttons[cur_view].source = self.src_selected

    def get_visible(self):
        return config.visible_cal

    def set_visible(self, new_view):
        prev_view = self.get_visible()
        
        self.buttons[prev_view].source = self.src_unselected
        self.buttons[new_view].source = self.src_selected
        config.visible_cal = new_view

    def add_toggle(self, mood):
        self.buttons[mood] = CalViewToggle(self, mood)

    def get_toggle(self, mood):
        return self.buttons[mood]


class CalViewToggle(ButtonBehavior, Image):
    def __init__(self, toggle_set, mood):
        super().__init__()
        self.toggle_set = toggle_set
        self.mood = mood
    
    def switch_views(self):
        self.toggle_set.set_visible(self.mood)
