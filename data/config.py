# pylint: disable=F0401

from data.mood import Mood
from pandas import Timestamp

# may want to keep things in a config.json to make this more easily customizable

# GLOBAL VARIABLES DEFINED:
# mood_data
#   Mood instance to be used by the program
# visible_cal
#   the mood currently visible on the calendar widget
# year
# month
#   the year and the month currently displayed on the calendar widget
#
#       might want to move these to the Calendar widget or the ViewScreen screen...


def init():

    global mood_data
    # can cange file locations here:
    mood_data = Mood("data/rates.csv", "data/weights.json")

    # indicates which mood is viewed in the calendar widget
    global visible_cal
    visible_cal = 'overall' # can change default here


    # indicate which month is currently being viewed:
    date = Timestamp.today()
    global year
    year = date.year

    global month
    month = date.month
