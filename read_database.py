import sqlite3
import json

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

c.execute("SELECT * FROM tweets")

# rows = c.fetchall()
# for row in rows:
# 	print(row)
var = json.dumps(c.fetchall())
print(var)