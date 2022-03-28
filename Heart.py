class Heart:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        
    def get_heart_data(self, date, period='1d'):
        return self.auth_client.time_series('activities/heart', base_date=date, period=period)
    
    @staticmethod
    def time_HR_zones(HRjson):
        hr_zones = ['Out of Range', 'Fat Burn', 'Cardio', 'Peak']
        hr_times = {}
        rel_json = HRjson['activities-heart'][0]['value']['heartRateZones']
        for component in rel_json:
            name = component['name']
            hr_times[name] = int(component['minutes'])
            
        oor_time = hr_times[hr_zones[0]]
        fb_time = hr_times[hr_zones[1]]
        c_time = hr_times[hr_zones[2]]
        p_time = hr_times[hr_zones[3]]
        return oor_time, fb_time, c_time, p_time
    
    
