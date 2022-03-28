import fitbit
import pandas as pd 
import datetime
import numpy as np
from Sleep import *
from Activity import *
from User import *
from Heart import *

class DataLoader:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        
    def authorize_client(self, access_token, refresh_token):
        self.auth2_client = fitbit.Fitbit(self.client_id, self.client_secret, oauth2=True, access_token=access_token, refresh_token=refresh_token)
        
    def get_sleep_data(self, start_date, num_days): 
        sleepLoader = Sleep(self.auth2_client)
        
        sleep_data = []
        sleep_headers = ['Date', 'MinutesAsleep', 'MinutesAwake', 'Awakenings', 'RestlessCount', 'RestlessDuration', 'Deep', 'Light', 'REM', 'Wake', 'StartTime', 'EndTime', 'MainDuration', 'SleepEfficiency','NumberOfSleepPeriods']
        for i in range(num_days):
            date_string = str((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            jsonSleep = sleepLoader.get_sleep_data(date_string)
            sleep_periods = len(jsonSleep['sleep'])
            try:
                main_sleep = jsonSleep['sleep'][0]
            except:
                entry = [date_string]
                sleep_data.append(entry)
                continue
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
        se = sleepLoader.get_sleep_efficiency(main_dict)
        dur = sleepLoader.get_main_sleep_duration(main_dict)
        
        data_list = [date, minutesasleep, minutesawake, awakenings, restless_count, restless_duration, deep, light, rem, wake, starttime, endtime, dur, se]
        return data_list
               
        
    def get_activity_data(self, start_date, num_days):
        activityLoader = Activity(self.auth2_client)
        
        activity_data = []
        activity_headers = ['NumActivities', 'activescore', 'activeCalories', 'caloriesBMR', 'caloriesOut', 'marginalCalories', 'restingHeartRate', 'Steps', 'lightlyActiveMinutes', 'veryActiveMinutes', 'sedentaryMinutes', 'fairlyActiveMinutes', 'Date']
        
        activityLoader = Activity(self.auth2_client)

        for i in range(num_days):
            date_string = str((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            jsonActivity = activityLoader.get_activity_data(date_string)
            entry = self.process_activity_data(activityLoader, jsonActivity)
            entry.append(date_string)
            activity_data.append(entry)
        return activity_data, activity_headers
    
    def process_activity_data(self, activityLoader, json):
        laMinutes, vaMinutes, sMinutes, faMinutes = activityLoader.get_minute_breakdowns(json)
        activecalories, caloriesBMR, caloriesOut, marginalCalories = activityLoader.get_calories_data(json)
        rhr = activityLoader.get_rhr(json)
        score = activityLoader.get_activity_score(json)
        total_steps = activityLoader.get_steps(json)
        numact = activityLoader.get_num_activities(json)
        print(json['summary']['sedentaryMinutes'])
        print(laMinutes, vaMinutes, sMinutes, faMinutes)
        return [numact, score, activecalories, caloriesBMR, caloriesOut, marginalCalories, rhr, total_steps, laMinutes, vaMinutes, sMinutes, faMinutes]
        
        
    def get_user_data(self):
        userLoader = User(self.auth2_client)
        userJson = userLoader.get_user_data()
        
        user_headers = ['Name', 'Birthday', 'Gender', 'SleepMode']
        user_data = []
        user_data.append(userLoader.get_user_name(userJson))
        user_data.append(userLoader.get_user_birthday(userJson))
        user_data.append(userLoader.get_user_gender(userJson))
        user_data.append(userLoader.get_user_sleep_tracking(userJson))
        return user_data, user_headers
    
    def get_heart_data(self, start_date, num_days):
        heartLoader = Heart(self.auth2_client)
        
        heart_headers = ['OutofRange', 'FatBurn', 'Cardio', 'Peak', 'Date']
        heart_data = []
        for i in range(num_days):
            date_string = str((start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))
            jsonHeart = heartLoader.get_heart_data(date_string)
            entry = self.process_heart_data(heartLoader, jsonHeart)
            entry.append(date_string)
            heart_data.append(entry)
        
        return heart_data, heart_headers
    
    def process_heart_data(self, heartLoader, json):
        oor_time, fb_time, c_time, p_time = heartLoader.time_HR_zones(json)
        return [oor_time, fb_time, c_time, p_time]
        
