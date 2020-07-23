from flask import Flask, jsonify, redirect, request, session, g
from flask_cors import CORS, cross_origin
import requests
import startup
import json 

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
  keys = startup.TOKEN_DATA
  auth_head = {"Authorization": "Bearer {}".format(keys[0])} 
  # get user info 
  user_info = requests.get('https://api.spotify.com/v1/me', headers=auth_head)
  return user_info.json()

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
  danceability = result['params']['danceability']
  energy = result['params']['energy']
  valence = result['params']['valence']
  popularity = result['params']['popularity']

  # format
  seed_genres = []
  seed_genres.append(genre)

  preferences = {
    'seed_genres' : seed_genres,
    'limit' : '10',
    'market': 'US',
    'target_danceability': danceability,
    'target_energy': energy,
    'target_valence': valence,
    'target_popularity': popularity
  }

  keys = startup.TOKEN_DATA
  auth_head = {"Authorization": "Bearer {}".format(keys[0])} 

  # get recommendations
  recommendations = requests.get('https://api.spotify.com/v1/recommendations', headers=auth_head, params=preferences)

  track_list = recommendations.json()['tracks']

  # make playlist
  # get user id 
  user = user_details().json
  user_id = user['id']

  # formulate headers
  playlist_headers = {
    "Authorization": "Bearer {}".format(keys[0]),
    "Content-Type": "application/json"
  }

  playlist_body = "{\"name\":\"Playlist by Vibeify\", \"description\":\"A playlist generated using Vibeify. Create a playlist to match your vibe at vibeify.herokuapp.com.\"}"
  
  # make playlist 
  playlist = requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(user_id), headers=playlist_headers, data=playlist_body)

  playlist_data = json.loads(playlist.text)

  playlist_id = playlist_data['id']

  #format 
  uris = ""

  for track in track_list:
    uris = uris + (track['uri']) + ','
  
  uris = uris[:-1]

  populate_playlist = requests.post('https://api.spotify.com/v1/playlists/{}/tracks?uris={}'.format(playlist_id, uris), headers=playlist_headers)
  
  return playlist.json()['external_urls']['spotify']
