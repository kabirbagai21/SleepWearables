import requests
import os

TokenURL = "https://api.fitbit.com/oauth2/token"

TokenFile = "/Users/kabirbagai/Desktop/Radicle-Sleep-Project/tokens.txt"

clientID = "2385BF"
clientSecret = "34dd55f271a7630dec75ba92f7b43413"
encodedID_Secret = 'MjM4NUJGOjM0ZGQ1NWYyNzFhNzYzMGRlYzc1YmE5MmY3YjQzNDEz'


AuthorizationCode = "b54ee9953e6d3f2c14e56abb8bb02818ff9ad138"

def WriteConfig(AccToken, RefToken):
     

  #Delete the old config file
  os.remove(TokenFile)

  #Open and write to the file
  FileObj = open(TokenFile,'w')
  FileObj.write(AccToken + "\n")
  FileObj.write(RefToken + "\n")
  FileObj.close()


def GetConfig():
      

  #Open the file
  FileObj = open(TokenFile,'r')

  #Read first two lines - first is the access token, second is the refresh token
  AccToken = FileObj.readline()
  RefToken = FileObj.readline()

  #Close the file
  FileObj.close()

  #See if the strings have newline characters on the end.  If so, strip them
  if (AccToken.find("\n") > 0):
    AccToken = AccToken[:-1]
  if (RefToken.find("\n") > 0):
    RefToken = RefToken[:-1]

  #Return values
  return AccToken, RefToken



#sends a post request to fitbit API with auth code in exchange for access tokens
def getAccessToken(authCode):

    BodyText = {'code' : authCode,
                'redirect_uri' : 'http://localhost',
                'client_id' : clientID,
                'grant_type' : 'authorization_code'}

    headers = {'Authorization': 'Basic ' + encodedID_Secret, 
        'Content-Type': 'application/x-www-form-urlencoded'}  


    req = requests.post(TokenURL, params=BodyText, headers= headers)

    postResponse = req.json() 

    access_token = postResponse['access_token']
    refresh_token = postResponse['refresh_token']

    WriteConfig(access_token, refresh_token)


def refreshAccessToken(refreshToken):
    BodyText = {'grant_type' : 'refresh_token', 'refresh_token' : refreshToken}

    headers = {'Authorization': 'Basic ' + encodedID_Secret, 
        'Content-Type': 'application/x-www-form-urlencoded'} 

    req = requests.post(TokenURL, params=BodyText, headers=headers)

    postResponse = req.json() 

    new_access_token = postResponse['access_token']
    new_refresh_token = postResponse['refresh_token']

    WriteConfig(new_access_token, new_refresh_token)


def APICall(access_token, refresh_token):
    header = {'Authorization' : 'Bearer {}'.format(access_token)}

    try:
        response = requests.get("https://api.fitbit.com/1/user/-/sleep/date/2022-03-21.json", headers = header)
        response.raise_for_status()

        response = response.json()
        for k, v in response.items():
            print(k)
            print(v)
            print("\n")


    except requests.exceptions.HTTPError as e:

        refreshAccessToken(refresh_token)
        new_result = GetConfig()
        new_access_token = new_result[0]
        new_refresh_token = new_result[1]
        APICall(new_access_token, new_refresh_token)


getAccessToken(AuthorizationCode)
result = GetConfig()
access_token = result[0]
refresh_token = result[1]
APICall(access_token, refresh_token)
