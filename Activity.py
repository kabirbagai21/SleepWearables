import pandas as pd
import datetime

class Activity:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        
    def get_activity_data(self, date):
        return self.auth_client.activities(date=date)
        
    @staticmethod
    def get_minute_breakdowns(json):
        lamin = int(json['summary']['lightlyActiveMinutes'])
        vamin = int(json['summary']['veryActiveMinutes'])
        smin = int(json['summary']['sedentaryMinutes'])
        famin = int(json['summary']['fairlyActiveMinutes'])

        return lamin, vamin, smin, famin
    
    @staticmethod
    def get_calories_data(json):
        try:
            activecalories = int(json['summary']['activityCalories'])
        except:
            activecalories = 0
        try:
            caloriesBMR = int(json['summary']['caloriesBMR'])
        except:
            caloriesBMR = 0
        try:
            caloriesOut = int(json['summary']['caloriesOut'])
        except:
            caloriesOut = 0
        try:
            marginalCalories = int(json['summary']['marginalCalories'])
        except:
            marginalCalories = 0

        return activecalories, caloriesBMR, caloriesOut, marginalCalories

    @staticmethod
    def get_activity_score(json):
        score = int(json['summary']['activeScore'])
        return score
    
    @staticmethod
    def get_rhr(json):
        try:
            rhr = int(json['summary']['restingHeartRate'])
        except:
            rhr = 0
        return rhr
    
    @staticmethod
    def get_steps(json):
        steps = int(json['summary']['steps'])
        return steps
    
    @staticmethod
    def get_num_activities(json):
        num_act = len(json['activities'])
        return num_act
        