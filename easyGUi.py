from easygui import *
import json
import tweepy
from tweepy import OAuthHandler
import re
import os
#from node import *

displayName=[]
rem=False
def parseTrend(names):
	global displayName
	#names = re.sub(r"u'#\\u[^\s]+", "",names)
	#print names
	for name in names :
		#name = re.sub(r"u'#\\u[^\s]+", "",name)
		if "#" not in name:
			names.remove(name)
			#print "hello"
			continue
		name = re.sub(r"(')", "", name)
		displayName.append(name.encode('utf-8'))
		
cKey="Co4urInLeO9hU3yiaPNvT2xRE"
cSecret="LZxYkwVj599yiycMyAROO8yu4xX4ZaP0i7DuWqJmpjZvq0WeyR"
aToken="2804705930-5WiAsst58UqqfnTtnCsKSvYyqy7ievxeBukR55n"
aSecret="6pAb8b0S2LB66Nr9GlHlxNmG9rrirEbBhJ79xBqUi2wer"
auth = OAuthHandler(cKey, cSecret)
auth.set_access_token(aToken, aSecret)
api = tweepy.API(auth)
trends1 = api.trends_place(1)


data = trends1[0] 
# grab the trends
trends = data['trends']


names = [trend['name'] for trend in trends]
#print names
parseTrend(names)

#print displayName

	
#tweet = re.sub(r"((\\n)|(\\u[\S]+)|(\brt\b)|(\\)|(\/)|(\.)|(\?)|(\!)|(\,))", "", tweet)
#resp_dict = json.loads(trends1)

#print resp_dict['name']




#msgbox("Tweet Analysis",title="Tweet Analysis")
msg = "Enter Keyword you want to analyse"
title = "Tweet Analysis"
#arrayy = ["ha", "HEH"]
choice = "Continue"
image = "twitterLogo.gif"

while choice != 'Quit':
        choice = buttonbox("Choose An Option", "Twitter Analysis", image = image,
                           choices=('Search', 'Trends', 'Quit'))
        if choice == 'Search':
                fieldNames = ["Keyword"]
                #fieldNames = ["blank"]
                fieldValues = [] # we start with blanks for the values
                fieldValues = multenterbox(msg,title, fieldNames)
                #arrayy.append(str(fieldNames))
                
                if fieldValues == ['']:
                        msgbox("Search Field Cannot Be Blank")
                for content in fieldValues:
                        if not content.isalpha():
                              msgbox("Please Enter Valid Search Term")
                        else:
                                filePath = ""
                                for content in fieldValues:
                                        filePath = filePath + content
                                
                                filePath = filePath + ".csv"
                                if os.path.isfile("twitter.csv"):
                                        os.remove("twitter.csv")
                                tweetCSV = open("twitter.csv", 'w')
                                tweetCSV.close()
                                code='Nodes.py'
                                #print(self.entry.get()+",you clicked the button!")
                                #os.system('python hello.py %(x)')
                                os.system("python {0} {1}".format(code, content))
                                #print "Reply was:", fieldValues
                        

                
        if choice == 'Trends':
                msgbox(displayName)

