# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, DictProperty

# PROJECT IMPORTS
import data.config as config
from ui.rateInput import RateInput

# OTHER IMPORTS
from pandas import isnull

class PopupMoodLabel(Label):
    pass

class PopupGrid(GridLayout):
    mood_cats = DictProperty()
    date = ObjectProperty()

    def __init__(self, date):
        super().__init__()
        self.mood_cats = config.mood_data.get_weights()
        self.date = date

        self.input_dict = {}
        # will store TextInput()'s corresponding to each mood

        for mood in self.mood_cats:
            self.add_row(mood)

        self.add_row('overall')
    
    def add_row(self,mood):
        mood_rating = config.mood_data.get_rate(mood,self.date)

        mood_label = PopupMoodLabel(text=mood)
        if mood == 'overall':
            mood_label.font_name = 'fonts/OpenSans-ExtraBold.ttf'
        self.add_widget(mood_label)

        if isnull(mood_rating):
            mood_rating = ''
        else:
            mood_rating = str(mood_rating)

        if mood =='overall':
            rate_label = PopupMoodLabel(
                text=mood_rating,
                size_hint_x=0.3,
                font_name = 'fonts/OpenSans-ExtraBold.ttf'
            )
            self.overall_label = rate_label
            self.input_dict[mood] = self.overall_label
        else:
            self.input_dict[mood] = RateInput(mood, mood_rating)
            
        self.add_widget(self.input_dict[mood])

    def save_mood_rate(self, mood):
        mood_rating = self.input_dict[mood].text

        if mood_rating != '':
            mood_rating = float(mood_rating)
            config.mood_data.update_rate(mood, self.date, mood_rating)

    def save_rates(self):
        for mood in self.input_dict:
            if mood == "overall":
                continue
            self.save_mood_rate(mood)

class EditRatePopup(Popup):
    cal_box = ObjectProperty()
    
    def __init__(self, cal_box):
        super().__init__()
        self.cal_box = cal_box
        self.content = PopupGrid(self.cal_box.date)
        
        date = self.cal_box.date.strftime("%B %d, %Y")
        self.title = date
    