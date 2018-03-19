#-*- coding: utf-8 -*-

import tweepy
import sqlite3

#Handling the API Access and setting up the connection
consumer_key = "dDg2wPt249fB87CI8SBDXOpet"
consumer_secret =  "YaNJ4iRphKxke41VpohtzVCOr5C55ljYtEbF1vAF93f80thvsl"
access_token = "2859636691-JyxcWeoUrjZc26L1tRL6QQquijNaLDgQ0Wfm0Jt"
access_token_secret = "ZXpYWICZrKZHIs1dBZboZrdBmMSrla0bxqaJRV0X79xj0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#Connects with the Database, if you haven't any database look at the SQLite 3 Tutorial how to create one using Python
conn = sqlite3.connect('Companie_Tweets.db')		
x = conn.cursor()
         
#Accounts nach Branche
kfz = ["vwpress_de", "BMWDeutschland", "OpelDE"]
chem = ["BASF_DE", "henkel_de", "HenkelPresse", "BoehringerDE"]
einzel = ["lidl", "SaturnDE", "REWE_Supermarkt"]
verkehr = ["Lufthansa_DE", "DB_Bahn", "DB_Presse", "DB_info", "FlixBus_DE"]
energie = ["innogy", "innogy_hilft", "EnBW", "EON_de", "EON_Sprecher"]
telko = ["telekomerleben", "telekomnetz", "Telekom_hilft", "vodafone_de", "vodafone_medien", "vodafoneservice", "o2de", "o2business"]					

#Accounts nach Unternehmen
vw = ["vwpress_de"]
bmw = ["BMWDeutschland"]
opel = ["OpelDE"]

basf = ["BASF_DE"]
henkel = ["henkel_de", "HenkelPresse"]
boehringer = ["BoehringerDE"]

lidl = ["lidl"]
saturn = ["SaturnDE"]
rewe = ["REWE_Supermarkt"]

lufthansa = ["Lufthansa_DE"]
bahn = ["DB_Bahn", "DB_Presse", "DB_Info"]
flixbus = ["FlixBus_DE"] 

rwe = ["innogy", "innogy_hilft"]
enbw = ["EnBW"]
eon = ["EON_de", "EON_Sprecher"]

telekom = ["telekomerleben", "telekomnetz", "Telekom_hilft"]
vodafone = ["vodafone_de", "vodafone_medien", "vodafoneservice"]
o2 = ["o2de", "o2business"]


#Liste der Database Namen
all_db1 = ["tkTelekom", "tkVodafone", "tkO2", "enEON", "enEnBW", "enRWE", "vkDB", "vkLufthansa", "vkFlixbus", "ehLidl", "ehSaturn", "ehRewe", "chBASF", "chBoehringer", "kfzVW", "kfzBMW", "kfzOpel"]

#Liste der Unternehmen mit Accounts
all_accounts1 = [telekom, vodafone, o2, eon, enbw, rwe, bahn, lufthansa, flixbus, lidl, saturn, rewe, basf, boehringer, vw, bmw, opel]

all_db = ["chBASF"]
all_accounts = [basf]

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

for i in range (0, len(all_db)):
	for account in all_accounts[i]:
		p = 0
		print "Datensätze für " + account + " werden heruntergeladen"
		for status in limit_handled(tweepy.Cursor(api.user_timeline, screen_name=account, max_id=936249373608030208, count=400).items()):
			# This block extracts the entities: Hashtags, Links and Mentions
			hashtag = ""
			urls= ""
			mentions = ""
			favorites = 0
			retweets = 0


			try:										
				for h in status.entities["hashtags"]:
					hashtag += h["text"] +" "
				for l in status.entities["urls"]:
					urls += l["expanded_url"] + " "
				for m in status.entities["user_mentions"]:
					mentions += m["id_str"] + " "  
			except:
				pass
				
			try:
				favorites = status.favorite_count
			except:
				pass
			try:
				retweets = status.retweet_count
			except:
				pass

			
			#SQLite Statement. If you want safe any other values it can be changed here, as long as your database is prepared for the new values.
			x.execute("INSERT INTO " + all_db[i] + "(ID, TimeStamp, User, Text, Favorites, Retweets, Hashtags, Links, Mentions, AnswerToTweet, AnswerToUser) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
			(status.id, status.created_at, status.user.id, status.text, favorites, retweets, hashtag, urls, mentions, status.in_reply_to_status_id, status.in_reply_to_user_id))
			conn.commit()
		p+=1	
		print account + " finished" + str(p) + " Accounts heruntergeladen"



