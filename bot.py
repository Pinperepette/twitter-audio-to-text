#!/usr/bin/python3

from tweepy import OAuthHandler, Stream, StreamListener
import json
import speech_recognition as sr
import time
import sys, os
from urllib.request import urlopen
import tweepy
from autex import get_status
from chiavi import *

class StdOutListener(StreamListener):

    def on_data(self, data):
        tw = json.loads(data)
        try:
            us = tw['user']['screen_name']
            tid = tw['id']
            try:
                tw_id = tw['quoted_status_id_str']
            except:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth) 
                messaggio = '@'+ us + ' ' + 'qualcosa non cosa, riprova'
                api.update_status(messaggio, in_reply_to_status_id = tid)
                tw_id = '0'
            
            if len(tw_id) != 0:
                get_status(int(tw_id), us, tid)
                os.system('rm /Users/thepirate/Desktop/test.wav')
        except:
            pass

    def on_error(self, status):
        print(status)

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['@pirate_bot_ai'])
