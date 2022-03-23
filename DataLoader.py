import fitbit
import pandas as pd 
import datetime
import numpy as np
from Sleep import *

class DataLoader:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def authorize_client(self, access_token, refresh_token):
        self.auth2_client = fitbit.Fitbit(self.client_id, self.client_secret, oauth2=True, access_token=access_token, refresh_token=refresh_token)
        
    def get_sleep_data(self, start_date, num_days): 
        sleepLoader = Sleep(self.auth2_client)
        
        sleep_data = []
        sleep_headers = ['Date', 'MinutesAsleep', 'MinutesAwake', 'Awakenings', 'RestlessCount', 'RestlessDuration', 'Deep', 'Light', 'REM', 'Wake', 'StartTime', 'EndTime', 'NumberOfSleepPeriods']
        for i in range(num_days):
            date_string = str((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            jsonSleep = sleepLoader.get_sleep_data(date_string)
            sleep_periods = len(jsonSleep['sleep'])     
            main_sleep = jsonSleep['sleep'][0]
            for i in range(sleep_periods):
                if jsonSleep['sleep'][i]['isMainSleep']:
                    main_sleep = jsonSleep['sleep'][i]
                    break           
            entry = self.process_sleep_data(sleepLoader,jsonSleep, main_sleep)
            entry.append(sleep_periods)
            sleep_data.append(entry)
        return sleep_data, sleep_headers
                           
    def process_sleep_data(self, sleepLoader, json, main_dict):
        date = sleepLoader.get_sleep_date(main_dict)
        minutesawake = sleepLoader.get_minutes_awake(json)
        minutesasleep = sleepLoader.get_minutes_asleep(json)
        starttime, endtime = sleepLoader.get_sleep_times(main_dict)
        awakenings = sleepLoader.get_num_awakenings(main_dict)
        wake, light, deep, rem = sleepLoader.get_sleep_stage_times(json)
        restless_count, restless_duration = sleepLoader.get_restless_statistics(main_dict)
        
        data_list = [date, minutesasleep, minutesawake, awakenings, restless_count, restless_duration, deep, light, rem, wake, starttime, endtime]
        return data_list
               
        
