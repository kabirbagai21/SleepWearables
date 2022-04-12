
from flask import Blueprint, redirect, render_template, request, flash
from .models import User, Tokens
from . import db
from flask_login import current_user, login_required, login_user
import requests
import csv
from csv import writer
views = Blueprint('views', __name__)

clientID = "2385BF"
clientSecret = "34dd55f271a7630dec75ba92f7b43413"
encodedID_Secret = 'MjM4NUJGOjM0ZGQ1NWYyNzFhNzYzMGRlYzc1YmE5MmY3YjQzNDEz'

TokenURL = "https://api.fitbit.com/oauth2/token"

def getAccessToken(authCode):
    
    BodyText = {'code' : authCode,
                'redirect_uri' : 'http://127.0.0.1:5000/final',
                'client_id' : clientID,
                'grant_type' : 'authorization_code'}

    headers = {'Authorization': 'Basic ' + encodedID_Secret, 
        'Content-Type': 'application/x-www-form-urlencoded'}  


    req = requests.post(TokenURL, params=BodyText, headers= headers)

    postResponse = req.json() 

    access_token = postResponse['access_token']
    refresh_token = postResponse['refresh_token']

    return access_token, refresh_token



def initCSV():
    
    filename = '/Users/kabirbagai/Desktop/Sleep Web App/users.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        fields = ['ID', 'Email', 'Auth Token', 'Refresh Token']
        writer.writerow(fields) 
        f.close()
        

def writeNewLine(current_user, new_tokens):
        filename = '/Users/kabirbagai/Desktop/Sleep Web App/users.csv'
        file = open(filename, "r")
        file_content = file.read()
        file.close()
        if file_content == "":
            initCSV()
            

        with open(filename, 'a+', newline='') as write_obj:
    
            csvwriter = writer(write_obj) 
            row = [str(current_user.id), current_user.email, new_tokens.auth_token, new_tokens.refresh_token]
            csvwriter.writerow(row)
        


def clearFile():
    filename = '/Users/kabirbagai/Desktop/Sleep Web App/users.csv'
    f = open(filename, "w+")
    initCSV()
    f.close()


@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
    
        else:
            new_user = User(email=email)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect("https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2385BF&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Ffinal&scope=activity%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&expires_in=604800")

    return render_template("home.html", user = current_user)



@login_required
@views.route('/final', methods=['GET', 'POST'])
def final():
   
    users = User.query.order_by(User.id);
    ts = Tokens.query.order_by(Tokens.user_id);
    

    if request.method == 'GET':
        code = request.args.get('code')
        

    
    tokens = getAccessToken(code)
    new_tokens = Tokens(auth_token = tokens[0], refresh_token = tokens[1], user_id = current_user.id)
    db.session.add(new_tokens)
    db.session.commit()
    
   
    writeNewLine(current_user, new_tokens)
    

    return render_template("final.html", user = current_user)





