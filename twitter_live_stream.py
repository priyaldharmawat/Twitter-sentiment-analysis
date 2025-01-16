from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s
import sqlite3

#consumer key, consumer secret, access token, access secret.
ckey="2skoxKQgrFHuFCyiyzIGuaxKQ"
csecret="qcL9mVyRGZhs7tWukO4i4HgjoaWirdMYFa5crGFr4UyqFlFJWM"
atoken="1131542924645134336-IKqILarxXSguU4wZileTnJlnKGdnJZ"
asecret="k3RT5nUes7CLxdJsdkdoTVGX6Su1lt2Eu2EleUwYO7WPp"

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

class listener(StreamListener):
	# output = open()

    def on_data(self, data):
    	all_data = json.loads(data)

    	tweet = all_data["text"]
    	# username = all_data["user"]["screen_name"]
    	userID = all_data["id"]

    	sentiment_value, confidence = s.sentiment(tweet)
    	print(tweet, sentiment_value, confidence)

    	if confidence*100 >= 80:
    		output = open("twitter-out.txt","a")
    		output.write(sentiment_value)
    		output.write('\n')
    		output.close()

    	c.execute("INSERT INTO tweets (ID, tweetText, sentiMent, Confidence) VALUES (?,?,?,?)",
            (userID, tweet, sentiment_value, confidence))
    	conn.commit()


    	return True

    def on_error(self, status):
    	# output.close()
    	if(status == 420):

    		return False

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Messi"])