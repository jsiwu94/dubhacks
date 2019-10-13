from flask import Flask, redirect, request, jsonify
from flask_cors import CORS
import twitter
import requests
import startup


from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


import pandas as pd
import numpy as np

from dateutil.parser import parse
from datetime import datetime


app = Flask(__name__)
cors = CORS(app)

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
    return ''


def getStuffFromTwitter(handle):
    twitter_api = twitter.Api(consumer_key=twitter_key,
consumer_secret=twitter_secret,
access_token_key=twitter_access_token_key,
access_token_secret=twitter_access_token_secret)

    all_tweets = []
    tweets = []
    if handle != '':

        try:
            user = twitter_api.GetUser(screen_name=handle)  # get user for max status count
        except twitter.error.TwitterError as te:
            if te.message[0]['code'] == 50:
                print('Error!', te.message[0]['message'])
            return

        print('Retrieving tweets.. ', end='')

        while True:
            last_id = tweets[len(tweets)-1].id if len(tweets) > 0 else None  # sets last_id to smallest status id or None if nonexistent

            tweets = twitter_api.GetUserTimeline(screen_name =handle, count=200, max_id=last_id-1 if type(last_id) is int else None, include_rts=False)  # list of Status objs

            all_tweets += tweets

            print('.. ', end='')
            if (user.statuses_count < 300 and len(all_tweets) == user.statuses_count) or len(all_tweets) >= 300:

                if len(all_tweets) >= 300:
                    all_tweets = all_tweets[0:300]
                print('Done.')
                break

            elif len(tweets) == 0:
                print('Maximum tweets retrieved.')
                break

        print('Total Tweet Count:', len(all_tweets))
        some_list = []
        # elon_timeline = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
        # print(len(elon_timeline))
        for status in all_tweets:
            text = status.full_text if status.full_text is not None else status.text
            text = ''.join(i for i in text if 32 <= ord(i) <= 90 or 97 <= ord(i) <= 122)
            some_list.append({
            'id' : status.id_str,
            'date' : status.created_at,
            'text' : text
            })
        
        return pd.DataFrame(some_list)
    else:
        print('not ok')
    return None #f'{some_list}'
    

def score_range(score):
    if score <= -.8:
        o = -.8
    elif score > -.8 and score <= -.5:
        o = -.5
    elif score > -.5 and score <= -.3:
        o = -.3
    elif score > -.3 and score <= .3:
        o = 0
    elif score > .3 and score <= .5:
        o = .3
    elif score > .5 and score <= .8:
        o = .5
    else:
        o = .8
    return(o)
    

@app.route('/api/twitter/')
def calculate_score():

    #fetching the data
    handle = request.args.get('twitter_handle', '')
    d = getStuffFromTwitter(handle)
    print(d)
    ##changing the date format
    date3 = []
    for i in range(d.shape[0]):
        a = parse(d.date[i])
        date2 = a.strftime("%Y-%m-%d")
        date3.append(date2)

    date3 = pd.DataFrame(date3)
    d2 = pd.concat([d, date3], axis = 1)
    d2.date = d2.iloc[:,[-1]]
    #source = ["twitter"]*len(d2)
    d2 = d2[['id', 'date', 'text']]
    d2['source'] = "twitter"

    client = language.LanguageServiceClient.from_service_account_json('/Users/Joshyy/Desktop/Projects/dubhacks/backend/second.json')

    ##calculating the score
    score = []
    for i in d2.text:
        text = i
        document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        score.append(sentiment.score)
            
    d2['score'] = score
    d2['score_range'] = d2.score.apply(score_range)

    output_1 = d2.groupby(['date'])['score_range'].agg(pd.Series.mode)

    output = output_1.reset_index(level=['date'])
    output['source']="twitter"
    output['score_range'] = output.score_range.apply(np.mean)
    print([i for i in output["date"]])
    print([i for i in output["score_range"]])
    return output.to_json()
