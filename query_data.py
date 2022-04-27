import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
from importlib import reload
import numpy as np
import DataLoader

CLIENT_ID = '2385BF'
CLIENT_SECRET = '34dd55f271a7630dec75ba92f7b43413'
STUDY_START_DATE = datetime.datetime.now() - datetime.timedelta(days=40)
AWS_PATH = '.'
FILE_OUTPUT_STRING = '{aws_path}/{study_name}/{participant_id}/{data_name}.csv'
DL = DataLoader.DataLoader(CLIENT_ID, CLIENT_SECRET)

def query_list_of_users(userList):
    current_date = datetime.datetime.now()

    for u in userList:
        user_email = u['user_email']
        access_token = u['access_token']
        refresh_token = u['refresh_token']
        start_date = get_last_entry_date(user_email, 'test') + datetime.timedelta(days=1)
        num_days = get_date_delta(start_date, current_date)
        data, headers = query_user_data(access_token, refresh_token, start_date, num_days))

        save_data_files(user_email, 'test', data, headers)

def query_user_data(access_token, refresh_token, start_date):
    DL.authorize_client(access_token, refresh_token)
    sleep_data,sleep_headers = dL.get_sleep_data(start_date, num_days)
    activity_data, activity_headers = DL.get_activity_data(start_date, num_days)
    heart_data, heart_headers = DL.get_heart_data(yesterday, 6)
    user_data, user_headers = DL.get_user_data()
    
    data = {'sleep': sleep_data,
            'activity': activity_data,
            'heart': heart_data,
            'user': user_data}
    headers = {'sleep': sleep_headers,
            'activity': activity_headers,
            'heart': heart_headers,
            'user': user_headers}

    return data, headers

def save_data_files(pid, study_namy,data, headers, DL):
    data_types = ['sleep', 'activity', 'heart', 'user']
    for dtype in data_types:
        df = pd.DataFrame(data[dtype], columns=headers[dtype])
        if os.path.isfile(FILE_OUTPUT_STRING.format(aws_path=AWS_PATH, study_name=study_name, participant_id=process_email(pid), data_name=dtype)):
            df.to_csv(FILE_OUTPUT_STRING.format(aws_path=AWS_PATH, study_name=study_name, participant_id=process_email(pid), data_name=dtype), mode='a', index=False, header=False
        else:
            df.to_csv(FILE_OUTPUT_STRING.format(aws_path=AWS_PATH, study_name=study_name, participant_id=process_email(pid), data_name=dtype), 
def get_last_entry_date(user_email, study_name):
    '''
    Finds the last entry date for a user to update file
    If no file exists, uses the study start date as the first date to query
    '''
    try:
        df = pd.read_csv(FILE_OUTPUT_STRING.format(aws_path=AWS_PATH, study_name=study_name, participant_id=process_email(user_email), data_name='sleep'))
    except:
        return STUDY_START_DATE
        
    dates = np.asarray(df['Date'])
    datetime_lst = []
    for d in dates:
        datetime_lst.append(datetime.strptime(d, '%Y-%m-%d'))

    datetime_lst.sort()
    return datetime_lst[-1]
    

def get_date_delta(date1, date2)
    delta = date2- date1
    return delta.days
def process_email(email):
    parts = email.split('@')
    return parts[0]
    
    
server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    
    sleep_data,headers = dl.get_sleep_data(start_date, num_days)
df = pd.DataFrame(sleep_data, columns=headers)
AWSpath = './'
studyname = 'test'
participantID = '1'
dl.save_data(df, AWSpath, studyname, participantID, 'sleep')


