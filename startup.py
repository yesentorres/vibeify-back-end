from flask_spotify_auth import getAuth, refreshAuth, getToken
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')

CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

CALLBACK_URL = 'http://localhost:3000'
# CALLBACK_URL = "https://vibeify.herokuapp.com"

SCOPE = "user-read-email playlist-modify-public playlist-modify-private"

#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}/callback".format(CALLBACK_URL), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}/callback".format(CALLBACK_URL))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
