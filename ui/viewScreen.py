# pylint: disable=F0401
# pylint: disable=no-member
# pylint: disable-msg=E0611

# KIVY IMPORTS
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

# PROJECT IMPORTS
from ui.calWidget import CalendarWidget
import data.config as config

# OTHER IMPORTS
from pandas import Timestamp, DateOffset

class MonthLabel(Label):
    def update_text(self):
        month_strs = [
            'January', 'February', 'March',
            'April', 'May', 'June',
            'July', 'August', 'September',
            'October', 'November', 'December'
        ]
        self.text = month_strs[config.month - 1] + " " + str(config.year)
    


class ViewScreenGrid(GridLayout):
    calendar = ObjectProperty()
    month_label = ObjectProperty()

    def on_kv_post(self, base_widget):
        self.draw_cal()

    def draw_cal(self):
        self.month_label.update_text()

        self.calendar = CalendarWidget()
        self.calendar.draw_cal()
        self.add_widget(self.calendar)
    
    def redraw_cal(self):
        self.remove_widget(self.calendar)
        self.draw_cal()

        
    def prev_month(self):
        if config.month == 1:
            config.year -= 1
            config.month = 12
        else:
            config.month -= 1
        
        self.redraw_cal()

    def next_month(self):
        # additionally, will return True if the viewed month
        # is the current month, and False otherwise

        this_month = Timestamp.today().replace(day=1).floor('D')
        month = DateOffset(months=1)
        
        cur_view = Timestamp(config.year,config.month,1)
        next_view = cur_view + month

        config.year = next_view.year
        config.month = next_view.month
        self.redraw_cal()

        return (next_view == this_month)
