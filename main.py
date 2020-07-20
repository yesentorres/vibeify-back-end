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
  return "success"

@app.route('/user-info', methods=['GET'])
@cross_origin()
def user_details():
  # breakpoint()
  keys = startup.TOKEN_DATA
  auth_head = {"Authorization": "Bearer {}".format(keys[0])} 
  # get user info 
  user_info = requests.get('https://api.spotify.com/v1/me', headers=auth_head)
  return user_info.json()['display_name']

@app.route('/get-genres', methods=['GET'])
@cross_origin()
def genre_seeds():
  keys = startup.TOKEN_DATA
  auth_head = {"Authorization": "Bearer {}".format(keys[0])} 
  # get genre seeds 
  genre_seeds = requests.get('https://api.spotify.com/v1/recommendations/available-genre-seeds', headers=auth_head)
  return genre_seeds.json()

@app.route('/recommendation-generator', methods=['POST'])
@cross_origin()
def get_recommendation():
  # parse user preferences 
  result = request.json
  genre = result['params']['genre_inspiration']
  # format
  seed_genres = []
  seed_genres.append(genre)

  preferences = {
    'seed_genres' : seed_genres,
    'limit' : '5'
  }

  keys = startup.TOKEN_DATA
  auth_head = {"Authorization": "Bearer {}".format(keys[0])} 

  # get recommendations
  recommendations = requests.get('https://api.spotify.com/v1/recommendations', headers=auth_head, params=preferences)


  return recommendations.json()