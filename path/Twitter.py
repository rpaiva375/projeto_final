#!/usr/bin/python
import tweepy
import csv #Import csv
import json
import re
import csv
import time
from kafka import KafkaProducer
import unicodedata
from json import dumps

def json_serializer(data):
    return json.dumps(data).encode("utf-8")
producer = KafkaProducer(bootstrap_servers=['localhost:9092'] , value_serializer=json_serializer)




def clean_tweet(tweet):
    tweet2 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str(tweet)).split())
    tweet3 = re.sub(r'^RT[\s]+', '', tweet2)
    return tweet3


def send_to_producer(tweeter):
    print(tweeter)
    return tweeter

auth = tweepy.auth.OAuthHandler('YCRvBi8r0LNZdb4WuYL4bNIEJ', 'VzdKny2yud9vahUfBdnYcJZmwAzFu4NC2KJmqTZEM5CBjSHbPZ')
auth.set_access_token('1401678034625761280-oCm6rlANlvljtBU5Eso8rQeTGYY5Ae', 'wdkiNklaqpCn4gKTzNd7x1WqZfWb5DOrY2n1LpUVSVz3W')

api = tweepy.API(auth)

# Open/create a file to append data to

#Use csv writer
search_words = ["i want to die","i dont want to live anymore","i will kill myself","fucking","anyone","bad","shit","tried","suicidal","pain","wish","enough","wanted","die","death","fuck","i dont care","i want to die","death"]
#search_words = ["eu quero morrer", "quero me matar","nao quero viver mais", "vou me matar", "viver", "porra", "qualquer um", "mau", "merda", "tentei", "suicida", "dor", "desejo", "suficiente", "queria", "morrer", "morte", "foda-se", "não me importo", "quero morrer"]
numberOfTweets = 10000
for x in search_words:
    print(x)
    for tweet in tweepy.Cursor(api.search,
                               q =  x,
                               geocode="-22.9110137,-43.2093727,600km",

                               # since = "2021-12-05",
                               #until = "2014-02-15",
                               lang = "en").items(400):

        time.sleep(1)
        twitter_limpo = clean_tweet(tweet.text)
        # Write a row to the CSV file. I use encode UTF-8
      #  csvWriter.writerow([tweet.user.screen_name,tweet.created_at, twitter_limpo])

        tweet.user.location = unicodedata.normalize("NFD", tweet.user.location)
        #Essa parte trata a acentuacao das cidades para não quebrar o código
       # print(tweet.user.location) # É o 5º e último. Estava 30°C
        tweet.user.location = tweet.user.location.encode("ascii", "ignore")
       # print(tweet.user.location) # b'E o 5 e ultimo. Estava 30C'
        tweet.user.location = tweet.user.location.decode("utf-8")
       # print(tweet.user.location) # E o 5 e ultimo. Estava 30C

        data = { 'tweet' : twitter_limpo,
                 'Localizacao' : tweet.user.location,
                 'Usuario' : tweet.user.screen_name,
                 'Data' : tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        print(data)
        producer.send("Analise-de-Twitter",data)