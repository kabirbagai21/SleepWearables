import pandas as pd
import datetime

class Sleep:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        
    def get_sleep_data(self, date):
        return self.auth_client.sleep(date=date)
        
    @staticmethod
    def get_minutes_awake(json):
        try:
            return int(json['summary']['totalTimeInBed']) - int(json['summary']['totalMinutesAsleep'])
        except:
            return 0
  
    @staticmethod
    def get_minutes_asleep(json):
        try:
            return int(json['summary']['totalMinutesAsleep'])
        except:
            return 0
        
    @staticmethod
    def get_sleep_times(main_sleep):
        try:
            start_time = main_sleep['startTime']
            end_time = main_sleep['endTime']
        except:
            start_time = 0
            end_time = 0
        return start_time, end_time

    @staticmethod
    def get_num_awakenings(main_sleep):
        try:
            return int(main_sleep['awakeningsCount'])
        except:
            return 0
    
    @staticmethod
    def get_sleep_date(main_sleep):
        try:
            return main_sleep['dateOfSleep']
        except:
            return "1900-00-00"
        
    @staticmethod
    def get_sleep_stage_times(json):
        try:
            deep = int(json['summary']['stages']['deep'])
            light = int(json['summary']['stages']['light'])
            rem = int(json['summary']['stages']['rem'])
            wake = int(json['summary']['stages']['wake'])
        except:
            deep = 0
            light = 0
            rem = 0
            wake = 0
        return wake, light, deep, rem
        
    @staticmethod
    def get_restless_statistics(main_sleep):
        try:
            restless_count = int(main_sleep['restlessCount'])
            restless_duration = int(main_sleep['restlessDuration'])
        except:
            restless_count =0 
            restless_duration = 0
        return restless_count, restless_duration
    
    @staticmethod
    def get_main_sleep_duration(main_sleep):
        try:
            dur = int(main_sleep['duration'])
        except: 
            dur = 0
        return dur
    
    @staticmethod
    def get_sleep_efficiency(main_sleep):
        try:
            se = float(main_sleep['efficiency'])
        except:
            se = 0.0
        return se
    
        
    