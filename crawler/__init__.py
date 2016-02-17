import sqlite3 as lite

con = lite.connect('crawler.db')	
with con:
	 cur = con.cursor()
	 cur.execute("CREATE TABLE IF NOT EXISTS RequestUrls(Id INTEGER PRIMARY KEY AUTOINCREMENT, requestUrl TEXT)")




