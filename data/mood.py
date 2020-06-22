#pylint: disable=F0401

import numpy as np
import pandas as pd
import json

class Mood:
    def __init__(self, csv_file_path, weights_path):
        self.file_path = csv_file_path
        self.weights_path = weights_path
        self.df = pd.read_csv(csv_file_path, parse_dates=True, index_col='date')

        with open(weights_path) as json_file:
            self.weights = json.load(json_file)

    def save_csv(self):
        sorted_df = self.df.dropna(how='all').sort_index()
        sorted_df.to_csv(self.file_path)
        with open(self.weights_path, "w") as json_file:
            json_file.write(json.dumps(self.weights))

    def get_weights(self):
       return self.weights

    def is_negative(self, mood):
        if mood=='overall': return False
        return self.weights[mood] < 0

    def update_rate(self, mood, date, rate):
        self.df.loc[date, mood] = rate
        self.df.loc[date, 'overall'] = self.get_overall(self.df.loc[date])

    def get_rate(self, mood, date):
        return self.df.loc[date, mood]

    def get_overall(self, row):
        # get_overall: dictionary -> float
        # takes a row from self.df and returns the weighted average,
        # ignoring all NaN entries

        val_sum = 0
        weight_total = 0

        for mood in self.weights:
            if pd.isnull(row[mood]): continue
            
            mood_weight = self.weights[mood]
            weight_total += abs(mood_weight)

            if mood_weight > 0:
                val_sum += mood_weight*row[mood]
            else:
                val_sum += abs(mood_weight)*(10-row[mood])

        if weight_total == 0:
            return np.nan
        return round( val_sum / weight_total, 2)

    def update_overall(self):
        # updates the 'overall' column of all
        self.df['overall'] = self.df.apply(self.get_overall, axis=1)

    def get_avr_all(self, mood):
        return self.df[mood].mean()
    
    def get_avr_month(self, mood):
        today = pd.Timestamp.today().floor('D')
        month_diff = pd.Timedelta(days=30)
        last_month = today - month_diff
        
        sliced_df = self.df.loc[last_month:today]
        return sliced_df[mood].mean()

    def populate_month(self, year, month):
        # ensures there is an entry for each day of the month in self.df
        # if an entry already exists, it is not changed
        # otherwise, creates an entry filled with NaN values

        num_days = pd.Timestamp(year, month, 1).days_in_month
        for day in range(1, num_days + 1):
            date = pd.Timestamp(year,month,day)
            if date in self.df.index: continue
            self.update_rate('overall', date, np.nan)
