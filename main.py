from flask import Flask, jsonify, redirect, request, session, g
from flask_cors import cross_origin
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
  global AUTH_CODE
  AUTH_CODE = result['params']['auth_code']['code']
  
  return 'got it'

@app.route('/user-info', methods=['GET'])
@cross_origin()
def user_details():
  startup.getUserToken(AUTH_CODE)
  access_code = startup.TOKEN_DATA[0]
  auth_head = {"Authorization": "Bearer {}".format(access_code)} 
  # get user info 
  user_info = requests.get('https://api.spotify.com/v1/me', headers=auth_head)
  return user_info.json()['display_name']

# @app.route('/recommendation-generator', methods=['POST'])
# @cross_origin()
# def get_recommendation():
#   # parse response
#   result = request.json

#   # set up preference params
#   preferences = {
    
#   }
#   # set up authorization header 
#   access_code = startup.TOKEN_DATA[0]
#   auth_head = {"Authorization": "Bearer {}".format(access_code)} 

#   # get recommendations
#   recommendation = requests.get('https://api.spotify.com/v1/recommendations?', headers=auth_head, params=preferences)