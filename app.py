from flask import Flask, render_template, current_app, redirect, url_for, session, request, jsonify
from requests_oauthlib import OAuth2Session
import os, time, json

app = Flask (__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

client_id = 'g105e5bab2115ec5a3de1b7fe6dacb'
client_secret = 'c9e172ded0'
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

    return redirect(url_for('token_view'))

@app.route('/zmview/', methods=['GET', 'POST'])
def token_view():

    zm = OAuth2Session(client_id,token=session['oauth_token'])
    s = session['oauth_token']
    c = zm.get('http://api.zenmoney.ru/v1/account?title=OPEN_FRTS').content
    return jsonify(s)

@app.route('/acc/', methods=['GET', 'POST'])
def account_view():

    zm = OAuth2Session(client_id,token=session['oauth_token'])
    
    data = {
        'currentClientTimestamp': int(time.time()),
        'serverTimestamp': int(0),
        'lastServerTimestamp': int(0)
        }

    c = zm.post("https://api.zenmoney.ru/v8/diff/",data=data)

    a = 1/0
    raise

    return 'Ohnoes'