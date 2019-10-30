#!/usr/bin/env python
# coding: utf-8

# In[40]:


#!/usr/bin/env python3
#Python twitter bot script test


#load packages

import json
import tweepy
import pymongo
import requests
import shutil
import os



from mongoengine import *
from pymongo import MongoClient
from PIL import Image
from langdetect import detect

#establishing data base connection


client = MongoClient('localhost', 27017)

db = client.magic_cards

cards_collection = db.cards_collection


# In[3]:


#trying credentials


# Authenticate to Twitter

#we create the link to the app in our twitter developer account to have access to the twitter API

#create OAuth:

auth = tweepy.OAuthHandler("mcEYPClyVOaoadcYtNQdFTHGr", # "CONSUMER_KEY"
    "U2dB7xoEuTH752wNUcFDuyAXtwsWl0Yy4LFdgsBIs8ZixYIwyI") # "CONSUMER_SECRET"


#The API class:

auth.set_access_token("1184771638874836993-wKQFq4A7DOXpnIRqRWSitzJKYmJBOS", # "ACCESS_TOKEN"
    "2GGAEo7xtHnrLHnU5az7xMXHEOkrh5clTlbjCcRoNWYe7") #"ACCESS_TOKEN_SECRET"

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
    


# In[3]:


# Create a tweet


#retrieve info for a random card
#we create it as a list to compensate for the not suscritable cursor object issue that comes with the aggregate function

random_card = list(cards_collection.aggregate([{'$sample': {'size':1}} ]))


#getting tweet image and saving it locally

#cleaning line for images

url = "" #empty

url = random_card[0]['image']

response = requests.get(url, stream=True)

with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

#resizing image for twitter format 

img = Image.open(r'C:\Users\riqui\Desktop\Python projects\Web scrapper\img.png')
img.thumbnail((512,1025), Image.ANTIALIAS)
img.save(r'C:\Users\riqui\Desktop\Python projects\Web scrapper\img.png', 'png', quality=88)


#creating tweet text :

card_name = random_card[0]['title'].replace(' ','').replace(',','').replace("'s","")

edition = random_card[0]['edition'].replace('#','Nº ')

card_type = random_card[0]['type of card']

hashtags = '#MTG #MagictheGathering #MTGArena #EDH'


#uploading tweet:


api.update_with_media(r'C:\Users\riqui\Desktop\Python projects\Web scrapper\img.png', 
                        status='Card name: #{}\nCard type: {}\nEdition: {}\n{}'.format(card_name,
                                                                                        card_type,                   
                                                                                        edition,
                                                                                        hashtags))

#erase the image

os.remove(r'C:\Users\riqui\Desktop\Python projects\Web scrapper\img.png')


# In[69]:


#behaviour part of the script for the bot


#Follow requests for people that follow the bot


for follower in tweepy.Cursor(api.followers).items(): 
    try:
        follower.follow()
    except:
        pass 
    
    
print ("Followed everyone that is following ")


# In[70]:


#retweets new tweets according to hashtags and english language according to hashtags


search = ['#MTG','#MTGArena','MagicTheGathering','#MTG #Commander','EDH']

number_of_tweets = 1 #can be adjsuted for content

for i in range(len(search)):
    for tweet in tweepy.Cursor(api.search, search[i]).items(number_of_tweets):  
        if detect(tweet.text) == 'en':
            try:       
                tweet.retweet()       
                print('Retweeted the tweet')
            except Exception as e:
                print(e)
                pass


# In[72]:


#retweets new tweets according to hashtags and english language according to hashtags


search = ['#MTG','#MTGArena','MagicTheGathering','#MTG #Commander','EDH']

number_of_tweets = 2 #can be adjsuted for content

for i in range(len(search)):
    for tweet in tweepy.Cursor(api.search, search[i]).items(number_of_tweets):  
        try:       
            tweet.favorite()       
            print('Liked the tweet')
        except:
            pass


# In[66]:




