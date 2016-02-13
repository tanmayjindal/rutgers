import re
import csv
from afinn import Afinn
#print ("Hello, Python!")

#import thread
#from Nodes import GUI
import time
import json
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import threading

#keyWord=str(sys.argv[1])

def processTweet(tweet):
    # process the tweets
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL edit by ankur
    tweet = re.sub('((www\.[^\s]+)|(https:[^\s]+))',' ',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #tweet = re.sub(r"\brt\b", "", tweet)
    tweet = re.sub(r"http\S+", "", tweet)
    #removes \n and anything start \u and remove RT
    tweet = re.sub(r"((\\n)|(\\u[\S]+)|(\brt\b)|(\\)|(\/)|(\.)|(\?)|(\!)|(\,))", "", tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet

def scoreUpdate(tweet):
    sentimentScore = Afinn()
    return sentimentScore.score(tweet)
#Authorization

'''guiInstance=GUI()
thread.start_new_thread(guiInstance.start,())
#guiInstance.start(distance=15, repulsion_radius=5)
#counter=0'''

class listener(StreamListener):
	tweetBody = None
	tweetId = 0
	sentimentScore = 0.0
	location = None
	print "Processing"
	def on_data(self,data):
		try:
			tweet=data.split(',"text":"')[1].split('","source')[0]
			tweet=processTweet(tweet)
			print tweet
			scoreTweet=scoreUpdate(tweet)
			#print tweet
			tweetId=data.split(',"id":')[1].split(',"id_str')[0]
			#print "."
			temp=[tweetId,scoreTweet,tweet]
			saveCSV=open('twitter.csv','a')
			wr = csv.writer(saveCSV, quoting=csv.QUOTE_ALL)
			wr.writerow(temp)
			saveCSV.close()
                        
			return True
		except BaseException ,e:
			print 'failed ondata,',str(e)
			time.sleep(5)
	def on_error(self,status):
		print status
#keywrd = "football"
def tweetStream(keywrd):
    cKey="Co4urInLeO9hU3yiaPNvT2xRE"
    cSecret="LZxYkwVj599yiycMyAROO8yu4xX4ZaP0i7DuWqJmpjZvq0WeyR"
    aToken="2804705930-5WiAsst58UqqfnTtnCsKSvYyqy7ievxeBukR55n"
    aSecret="6pAb8b0S2LB66Nr9GlHlxNmG9rrirEbBhJ79xBqUi2wer"
    auth = OAuthHandler(cKey, cSecret)
    auth.set_access_token(aToken, aSecret)
    twitterStream = Stream(auth, listener())
    #This line filter Twitter Streams to capture data by the keywords: 'football', 'java', 'DemDebate'
    twitterStream.filter(track=[keywrd])

#tweetStream(keywrd)  
