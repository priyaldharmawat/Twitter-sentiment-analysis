import sqlite3

conn = sqlite3.connect('twitter.db')
c = conn.cursor()
c.execute('''CREATE TABLE tweets
			(ID text,
			 tweetText text,
			 sentiMent text,
			 Confidence text)''')
conn.commit()
conn.close()