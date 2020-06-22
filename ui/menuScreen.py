# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.gridlayout import GridLayout
from kivy.properties import DictProperty
from kivy.uix.label import Label

# PROJECT IMPORTS
from ui.calViewSelect import CalViewToggleSet
import data.config as config

class RateLabel(Label):
    pass

class MenuMoodLabel(Label):
    pass

class MenuGrid(GridLayout):
    mood_rows = DictProperty()

    def on_kv_post(self, base_widget):
        mood_cats = config.mood_data.get_weights()
        self.toggles = CalViewToggleSet()

        for mood in mood_cats:
            self.add_row(mood, mood_cats[mood])
        self.add_row("overall", 0)
        
    def add_row(self, mood, weight):
        self.mood_rows[mood] = MenuRow(mood, weight, self.toggles)
        self.add_widget(self.mood_rows[mood])
    
    def refresh(self):
        for mood in self.mood_rows:
            self.mood_rows[mood].calculate_avs()



class MenuRow(GridLayout):
    def __init__(self, mood, weight, toggle_set):
        super().__init__()
        self.mood = mood

        self.add_widget(toggle_set.get_toggle(mood))
        self.add_widget(MenuMoodLabel(text=mood))

        self.tot_av_label = RateLabel()
        self.add_widget(self.tot_av_label)

        self.month_av_label = RateLabel()
        self.add_widget(self.month_av_label)

        self.calculate_avs()

        if (mood != 'overall'):
            self.add_widget(RateLabel(text=str(weight)))
        else:
            self.add_widget(RateLabel(text=''))
    
    def calculate_avs(self):
        tot_av = config.mood_data.get_avr_all(self.mood)
        tot_av = round(tot_av, 2)
        self.tot_av_label.text = str(tot_av)

        month_av = config.mood_data.get_avr_month(self.mood)
        month_av = round(month_av, 2)
        self.month_av_label.text = str(month_av)
