from flask import Flask, redirect, request
import twitter
import requests
import startup
app = Flask(__name__)

twitter_key = 'zJLt4JORP1zSLnkCRhLbtocWI'
twitter_secret = 'rHcB486RoNjxKftLJcitsBGkrGGMqmrho0VMJ4vEhgfpPmq6G4'
twitter_access_token_key = '425447793-2BkGFfpkjpVSiSPHKJYIKbOcpPvbb457TNbLMVR2'
twitter_access_token_secret = '7FJztNRybT4VKAJJYB9YlAlPgyvQ6ntj7L54sJngLW0Hd'

#spotify_client_id = 'c5ea6d4743ed4ea4b74d2379152156a8'
#spotify_base_url = 'https://api.spotify.com'
#
#
#@app.route('/')
#def hello_world():
#    return 'Hello, World!'
#
#@app.route('/api/spotify/')
#def auth_spotify_redirect():
#    response = startup.getUser()
#    return redirect(response)
##
##    payload = {
##    'client_id' : spotify_client_id,
##    'response_type' : 'code',
##    'redirect_uri' : 'http://localhost:5000/api/spotify/callback',
##    'scope': 'user-library-read'
##    }
##    r = requests.get('https://accounts.spotify.com/authorize', params=payload)
##    print(r.text)
##    return (r.text)
#
#@app.route('/api/spotify/callback/')
#def auth_spotify_callback():
#    startup.getUserToken(request.args['code'])
#    print("ADSADS")
#    return b''


@app.route('/')
def index():
    
    getStuffFromTwitter()
    return ''


def getStuffFromTwitter():
    twitter_api = twitter.Api(consumer_key=twitter_key,
consumer_secret=twitter_secret,
access_token_key=twitter_access_token_key,
access_token_secret=twitter_access_token_secret)
    
    
    some_list = []
    elon_timeline = twitter_api.GetUserTimeline(screen_name='elonmusk', count=200, include_rts=False)
    for status in elon_timeline:
        some_list.append({
        'id' : status.id_str,
        'date' : status.created_at,
        'text' : status.full_text if status.full_text is not None else status.text
        })
    print(some_list)
    return ''
    
