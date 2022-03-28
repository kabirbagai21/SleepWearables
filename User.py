class User:
    def __init__(self, auth_client):
        self.auth_client = auth_client
        
    def get_user_data(self):
        data = self.auth_client.user_profile_get()
        return data
    
    @staticmethod
    def get_user_name(json):
        return json['user']['fullName']
    
    @staticmethod
    def get_user_birthday(json):
        return json['user']['dateOfBirth']
    
    @staticmethod
    def get_user_gender(json):
        return json['user']['gender']
    
    @staticmethod
    def get_user_sleep_tracking(json):
        return json['user']['sleepTracking']