#!/usr/bin/python3

import json
import speech_recognition as sr
import time
import sys, os
from urllib.request import urlopen
import tweepy
from chiavi import *

def get_status(id, us, tid):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth) 

    tweet = api.get_status(id = id)
    json_str = json.dumps(tweet._json)
    tw = json.loads(json_str)
    cwd = os.getcwd()

    for x in tw['extended_entities']['media']:
        url = x['video_info']['variants'][1]['url']
        
    mp4file = urlopen(url)

    with open("test.mp4", "wb") as handle:
        handle.write(mp4file.read())
        
    file_in = cwd+'/test.mp4'

    command = str('ffmpeg -i '+ file_in + ' -vn -acodec pcm_s16le -ar 44100 -ac 2 test.wav')
        
    os.system(command)

    time.sleep(10)

    r = sr.Recognizer()
    wav = sr.AudioFile('/Users/thepirate/Desktop/test.wav')
    print(wav)
    
    with wav as source:
        r.pause_threshold = 3.0
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio,language= 'it-IT')
        if len(text) >= 240:
            testo = '@'+ us + ' ' + 'coccodio il testo è troppo lungo'
            api.update_status(testo, in_reply_to_status_id = tid)
        else:
            print(text)
            testo = '@'+ us + ' ' + text
            api.update_status(testo, in_reply_to_status_id = tid)

    except Exception as e:
        print(e)
