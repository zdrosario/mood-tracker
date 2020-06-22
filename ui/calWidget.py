# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color
from kivy.properties import ObjectProperty

# PROJECT IMPORTS
import data.config as config
from ui.editRatePopup import EditRatePopup

# OTHER IMPORTS
from pandas import Timestamp, isnull

class CalBox(Button):

    def __init__(self, date):
        self.date = date
        self.cur_mood = config.visible_cal
        self.rate = config.mood_data.get_rate(self.cur_mood, self.date)
        super().__init__(text=str(self.date.day))
        
        today = Timestamp.today().floor('D')
        if self.date > today:
            self.disabled=True

        if isnull(self.rate): return
    
        if config.mood_data.is_negative(self.cur_mood):
            self.rate = 10 - self.rate

        self.background_color = self.rate_to_color()
        self.color = [0.976,0.969,0.929,1]
    
    def update_box(self):
        self.rate = config.mood_data.get_rate(self.cur_mood, self.date)
        if isnull(self.rate): return
        if config.mood_data.is_negative(self.cur_mood):
            self.rate = 10 - self.rate
        self.background_color = self.rate_to_color()
        self.color = [0.976,0.969,0.929,1]

    def attempt_popup(self):
        popup_window = EditRatePopup(self)
        popup_window.open()
         
    def rate_to_color(self):
        # rate_to_color -> [r, g, b, a]
        # color has the HSV format ((self.rate-1)*12, 70, 85)

        hue = (self.rate - 1) * 12
        sat = 0.7
        val = 0.85

        C = sat*val
        X = C * (1 - abs((hue / 60) % 2 - 1))
        m = val - C

        if (self.rate < 5):
            return [C + m, X + m, m, 1]
        else:
            return [X + m, C + m, m, 1]

class CalendarWidget(GridLayout):
    def draw_cal(self):
        month_first = Timestamp(config.year,config.month,1)
        month_day_start = month_first.dayofweek
        # note: monday = 0
        days_in_month = month_first.daysinmonth

        # fills the empty days before the month starts
        for _ in range(month_day_start):
            self.add_widget(Label(text=''))

        config.mood_data.populate_month(config.year, config.month)
        # ensures we don't get dataframe access errors

        for day in range(1, days_in_month + 1):
            date=Timestamp(config.year,config.month,day)
            cal_box = CalBox(date)
            self.add_widget(cal_box)
