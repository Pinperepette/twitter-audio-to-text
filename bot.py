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
            user_id = tw['user']['screen_name']
            tid = tw['id']
            try:
                tw_id = tw['quoted_status_id_str']
            except:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth) 
                messaggio = '@'+ user_id + ' ' + 'qualcosa non cosa, riprova'
                api.update_status(messaggio, in_reply_to_status_id = tid)
                tw_id = '0'
            
            if len(tw_id) != 0:
                get_status(int(tw_id), us, tid)
                os.system('rm /Users/thepirate/Desktop/test.wav')
        except:
            pass

    def on_error(self, status):
        print(status)
    
    '''    
    #Split plain text into an array of tweet's corpus (max 280 characters)    
    def split_text_into_tweets2(text):
        MAX_LENGTH = 280
        
        if len(text) > MAX_LENGTH:
            result = []
            while len(text) > MAX_LENGTH and len(text.strip()) > 0 :
                result.append(text[:MAX_LENGTH])
                text = text[MAX_LENGTH:]
            return result
        else:
            return [text]
    '''
        
    #Split plain text into an array of tweet's body (max 280 characters)    
    def split_text_into_tweets(text):
        MAX_LENGTH = 280
        
        if len(text) > MAX_LENGTH:
            result = []
            text = text.split()
            index = 0
            while index < len(text):
                tweet = []
                ok = True
                while ok:
                    still_words = index <= len(text) - 1
                        #tweet's words    |    spaces      |   new word
                    if still_words and sum(list(map(len,tweet))) + len(tweet) + len(text[index]) <= MAX_LENGTH:
                        tweet.append(text[index])   
                        index += 1
                    else:
                        ok = False
                #append tweet to result
                tweet = ' '.join(tweet)
                result.append(tweet)
                
            return result
                
        else:
            return [text]

if __name__ == '__main__':

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['@pirate_bot_ai'])
