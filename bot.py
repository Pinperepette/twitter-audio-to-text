#!/usr/bin/python3
from tweepy import OAuthHandler, Stream, StreamListener
import json
import speech_recognition as sr
import time
import sys, os
from urllib.request import urlopen
import tweepy

consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

class StdOutListener(StreamListener):

    def get_status(self, id, us, tid):
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
            print(text)
            testo = '@'+ us + ' ' + text
            api.update_status(testo, in_reply_to_status_id = tid)

        except Exception as e:
            print(e)

    def on_data(self, data):
        tw = json.loads(data)
        tw_id = tw['quoted_status_id_str']
        us = tw['user']['screen_name']
        tid = tw['id']
        self.get_status(int(tw_id), us, tid)
        os.system('rm /Users/thepirate/Desktop/test.wav')


    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['@pirate_bot_ai'])
