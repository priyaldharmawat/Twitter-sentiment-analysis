from flask import Flask, redirect, url_for
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime as dt
import sentiment_mod as s
import sqlite3
import json


app = Flask(__name__)

ckey="2skoxKQgrFHuFCyiyzIGuaxKQ"
csecret="qcL9mVyRGZhs7tWukO4i4HgjoaWirdMYFa5crGFr4UyqFlFJWM"
atoken="1131542924645134336-IKqILarxXSguU4wZileTnJlnKGdnJZ"
asecret="k3RT5nUes7CLxdJsdkdoTVGX6Su1lt2Eu2EleUwYO7WPp"

#Creating Database
# conn = sqlite3.connect('twitter.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE tweets
# 			(ID text,
# 			 tweetText text,
# 			 sentiMent text,
# 			 Confidence text)''')
# conn.commit()
# conn.close()

##########
# conn = sqlite3.connect('twitter.db')
# c = conn.cursor()

class listener(StreamListener):
	# output = open()
	# conn = sqlite3.connect('twitter.db')
	# c = conn.cursor()

	def __init__(self, time_limit):
		self.start_time = int(dt.now().strftime("%S"))
		self.limit = time_limit
		super(listener, self).__init__()

	def on_data(self, data):
		if(int(dt.now().strftime("%S")) - self.start_time) < self.limit:
			conn = sqlite3.connect('twitter.db')
			c = conn.cursor()

			all_data = json.loads(data)
			tweet = all_data["text"]
			userID = all_data["id"]
			sentiment_value, confidence = s.sentiment(tweet)


			c.execute("INSERT INTO tweets (ID, tweetText, sentiMent, Confidence) VALUES (?,?,?,?)",
					(userID, tweet, sentiment_value, confidence))
			conn.commit()

			print(tweet, sentiment_value, confidence)


			if confidence*100 >= 80:
				output = open("twitter-out.txt","a")
				output.write(sentiment_value)
				output.write('\n')
				output.close()
			return True
		else:
			return False

	def on_error(self, status):
		if(status == 420):
			return False

@app.route('/get_keyword', methods = ['GET'])
def keyword():
	kWord = "Trump"
	return redirect(url_for("abc",kWord = kWord))


@app.route('/twitter_stream/<kWord>',  methods = ['GET'])
def abc(kWord):
	# conn = sqlite3.connect('twitter.db')
	# c = conn.cursor()
	print(kWord)
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	twitterStream = Stream(auth, listener(time_limit = 5))
	twitterStream.filter(track=[kWord])
	return 'Loop Completed.'

@app.route('/database_read', methods = ['GET'])
def hello():
	conn = sqlite3.connect('twitter.db')
	c = conn.cursor()

	c.execute("SELECT * FROM(SELECT * FROM tweets ORDER BY ID DESC LIMIT 5)")
	# rows = c.fetchall()
	# for row in rows:
	# 	print(row)

	var = json.dumps(c.fetchall())
	# print(var)

	return var
if __name__ == '__main__':

	app.run(debug = True)