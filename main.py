from flask import Flask, jsonify, redirect, request, session, g
from flask_cors import CORS, cross_origin
import requests
import startup

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
  response = startup.getUser()
  return redirect(response)

@app.route('/access', methods=['POST'])
@cross_origin()
def get_access(): 
  result = request.json
  auth_code = result['params']['auth_code']['code']
  startup.getUserToken(auth_code)
  return 'got it'

@app.route('/user-info', methods=['GET'])
@cross_origin()
def user_details():
  access_code = startup.TOKEN_DATA[0]
  auth_head = {"Authorization": "Bearer {}".format(access_code)} 
  user_info = requests.get('https://api.spotify.com/v1/me', headers=auth_head)
  return user_info.json()['display_name']
