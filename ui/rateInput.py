# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

# PROJECT IMPORTS
import data.config as config

# OTHER IMPORTS
import re

class RateInput(TextInput):
    mood = StringProperty()

    def __init__(self, mood, mood_rating):
        super().__init__(text=mood_rating)
        self.mood = mood

    def insert_text(self, substring, from_undo=False):
        pat = re.compile('[^0-9]')
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(RateInput, self).insert_text(s, from_undo=from_undo)  

    def save(self):
        self.parent.save_mood_rate(self.mood)
        mood_rating = config.mood_data.get_rate('overall',self.parent.date)
        self.parent.overall_label.text = str(mood_rating)
