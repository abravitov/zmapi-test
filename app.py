from flask import Flask, render_template, current_app, redirect, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session
import os, time, json

app = Flask (__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

client_id = '************'
client_secret = '**********'
authorization_base_url = "https://api.zenmoney.ru/oauth2/authorize/"
token_url = "https://api.zenmoney.ru/oauth2/token/"
redirect_uri = 'http://localhost:5000/callback'


@app.route('/', methods=['GET', 'POST'])
def index():
    zm = OAuth2Session(scope=None,client_id=client_id,redirect_uri=redirect_uri)
    authorization_url, state = zm.authorization_url(authorization_base_url)
    session['oauth_state'] = state

    return redirect(authorization_url)


@app.route('/callback', methods=['GET'])
def callback():
    
    zm = OAuth2Session(client_id,state=session['oauth_state'],redirect_uri=redirect_uri)
    token = zm.fetch_token(token_url,client_secret=client_secret,authorization_response=request.url)

    session['oauth_token'] = token

    return redirect(url_for('account_view'))

@app.route('/zmview/', methods=['GET', 'POST'])
def token_view():

    zm = OAuth2Session(client_id,token=session['oauth_token'])
    s = session['oauth_token']
    return jsonify(s)

@app.route('/acc/', methods=['GET', 'POST'])
def account_view():

    zm = OAuth2Session(client_id,token=session['oauth_token'])
    
    data = {
        'currentClientTimestamp': int(time.time()),
        'serverTimestamp': int(0)
        }

    data = json.dumps(data) # Необходимая конвертация для API

    c = zm.post("https://api.zenmoney.ru/v8/diff/",data=data,headers={"Content-Type": "application/json"})

    json_dump = json.loads(c.content)

    with open('zmpdump.json', 'w+') as f:
        json.dump(json_dump, f, ensure_ascii=False)
        f.close()

    return "The data has been updated"
