# KIVY IMPORTS
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# PROJECT IMPORTS
import data.config as config
from data.mood import Mood

class MTScreenManager(ScreenManager):
    pass

class Tracker(App):
    def build(self):
        config.init()
        self.screenmanager = MTScreenManager() 
        return self.screenmanager
    
    def on_stop(self):
        config.mood_data.save_csv()


if __name__ == '__main__': 
    Tracker().run()
