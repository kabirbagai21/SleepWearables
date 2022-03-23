import pandas as pd

class Sleep:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        
    def get_sleep_data(self, date):
        return self.auth_client.sleep(date=date)
        
    @staticmethod
    def get_minutes_awake(json):
        return int(json['summary']['totalTimeInBed']) - int(json['summary']['totalMinutesAsleep'])
  
    @staticmethod
    def get_minutes_asleep(json):
        return int(json['summary']['totalMinutesAsleep'])
        
    @staticmethod
    def get_sleep_times(main_sleep):
        start_time = main_sleep['startTime']
        end_time = main_sleep['endTime']
        return start_time, end_time

    @staticmethod
    def get_num_awakenings(main_sleep):
        return int(main_sleep['awakeningsCount'])
    
    @staticmethod
    def get_sleep_date(main_sleep):
        return main_sleep['dateOfSleep']
        
    @staticmethod
    def get_sleep_stage_times(json):
        deep = int(json['summary']['stages']['deep'])
        light = int(json['summary']['stages']['light'])
        rem = int(json['summary']['stages']['rem'])
        wake = int(json['summary']['stages']['wake'])
        return wake, light, deep, rem
        
    @staticmethod
    def get_restless_statistics(main_sleep):
        restless_count = int(main_sleep['restlessCount'])
        restless_duration = int(main_sleep['restlessDuration'])
        return restless_count, restless_duration
    
        
    