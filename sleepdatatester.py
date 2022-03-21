import requests


TokenURL = "https://api.fitbit.com/oauth2/token"

clientID = "2385BF"
clientSecret = "34dd55f271a7630dec75ba92f7b43413"
encodedID_Secret = 'MjM4NUJGOjM0ZGQ1NWYyNzFhNzYzMGRlYzc1YmE5MmY3YjQzNDEz'


AuthorizationCode = "51a3282d9dfc572bf44789096420197e556a5eaa"


BodyText = {'code' : AuthorizationCode,
            'redirect_uri' : 'http://localhost',
            'client_id' : clientID,
            'grant_type' : 'authorization_code'}

headers = {'Authorization': 'Basic ' + encodedID_Secret, 
    'Content-Type': 'application/x-www-form-urlencoded'}  


req = requests.post(TokenURL, params=BodyText, headers= headers)

postResponse = req.json() 

access_token = postResponse['access_token']

header = {'Authorization' : 'Bearer {}'.format(access_token)}
response = requests.get("https://api.fitbit.com/1/user/-/sleep/date/2022-03-21.json", headers = header).json()



for k, v in response.items():
    print(k)
    print(v)
    print("\n")
