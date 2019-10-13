
from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "c5ea6d4743ed4ea4b74d2379152156a8"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "cbe21aec02674ccd8bd9cb27336a9846"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "5000/api/spotify"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = "user-library-read"
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []


def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
