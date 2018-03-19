# -*- coding: utf-8 -*-
#
#  Auswertung.py
#  
#  Copyright 2018 Nils <Nils@VAIO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  


import sqlite3
import tweepy
import nltk
import operator
import datetime
import matplotlib.pyplot as plt
import xlwt
import scipy
from tempfile import TemporaryFile
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud, STOPWORDS

consumer_key = "dDg2wPt249fB87CI8SBDXOpet"
consumer_secret =  "YaNJ4iRphKxke41VpohtzVCOr5C55ljYtEbF1vAF93f80thvsl"
access_token = "2859636691-JyxcWeoUrjZc26L1tRL6QQquijNaLDgQ0Wfm0Jt"
access_token_secret = "ZXpYWICZrKZHIs1dBZboZrdBmMSrla0bxqaJRV0X79xj0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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
dkfz =["kfzVW","kfzBMW","kfzOpel"]
denergie=["enEON","enEnBW","enRWE"]
deinzelhandel=["ehLidl","ehSaturn","ehRewe"]
dverkehr=["vkDB","vkLufthansa","vkFlixbus"]
dchemie=["chBASF","chHenkel","chBoehringer"]
dtelko=["tkTelekom","tkVodafone","tkO2"]

all_db = ["tkTelekom", "tkVodafone", "tkO2", "enEON", "enEnBW", "enRWE", "vkDB", "vkLufthansa", "vkFlixbus", "ehLidl", "ehSaturn", "ehRewe", "chBASF", "chHenkel", "chBoehringer", "kfzVW", "kfzBMW", "kfzOpel"]
db_industry = [dkfz, denergie, deinzelhandel, dverkehr, dchemie, dtelko]
industry_names= ["KFZ","Energie","Einzelhandel","Verkehr","Chemie","Telekommunikation"]
#Liste der Unternehmen mit Accounts
all_accounts = [telekom, vodafone, o2, eon, enbw, rwe, bahn, lufthansa, flixbus, lidl, saturn, rewe, basf, henkel, boehringer, vw, bmw, opel]



def cloud(c):
	c.execute("""	SELECT Text
					FROM alle""")
					
	result = c.fetchall()
	text = ""
	for tweet in result:
		text += str(tweet[0].encode("utf-8"))+ " "
	text = text.lower()
	stopwords = set(STOPWORDS)
	stopword_list_everytime =["https", "via", "amp", "co", "will", "de"]

	for s in stopword_list_german:
		stopwords.add(s)
		
	for s in stopword_list_everytime:
		stopwords.add(s)
				
	wordcloud = WordCloud(max_font_size=100, stopwords=stopwords).generate(text)
	
	
	plt.figure()
	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

def most_common_hashtags(c):
	c.execute("""	SELECT Text, Hashtags
					FROM alle""")
	result = c.fetchall()
	text = ""
	
	for tweet in result:
		text += str(tweet[1].encode("utf-8")) + " "
	text = text.lower()
	
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(text)
	frequency = nltk.FreqDist(words)
	sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
	for i in range(-1,-50,-1):
		print sorted_frequency[i]	

def language_analyse(d):
	d.execute(""" SELECT Count(*), Category 
					FROM kfzVW
					GROUP BY Category
					HAVING category != 'null'
					ORDER BY Count(*) DESC
					""")
					
	result = d.fetchall()
	categories = []
	counts = []
	
	for line in result:
		counts.append(line[0])
		categories.append(line[1])
	labels = categories
	
	fig1, ax1 = plt.subplots()
	
	ax1.pie(counts, labels = labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
	ax1.axis("equal")
	
	plt.show()


def unternehmen_summiert():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Auswertung")

	Sheet.write(0,0,"Company")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Count")
	Sheet.write(0,3,"Favorites")
	Sheet.write(0,4,"Retweets")
	Sheet.write(0,5,"Fav/Count")
	Sheet.write(0,6,"ReT/Count")

	z = 1
	for db in all_db:
		SC = 0
		SF = 0
		SR = 0
		kC = 0
		kF = 0
		kR = 0
		x.execute(""" SELECT Category, COUNT(Category), SUM(Favorites), SUM(Retweets) FROM """ +db+ """ WHERE Category != "null" AND Category != "RT" GROUP BY Category ORDER BY Count(Category) DESC""")
		result = x.fetchall()
		Sheet.write(z,0,db)
		for r in result:
			Sheet.write(z,1,r[0])
			Sheet.write(z,2,r[1])
			Sheet.write(z,3,r[2])
			Sheet.write(z,4,r[3])
			SC+=r[1]
			SF+=r[2]
			SR+=r[3]
			if r[1] < 25: 
				kC+=r[1]
				kF+=r[2]
				kR+=r[3]
			z += 1
		Sheet.write(z,1,"Sonstiges")
		Sheet.write(z,2,kC)
		Sheet.write(z,3,kF)
		Sheet.write(z,4,kR)
		z+=1
		Sheet.write(z,1,"Summe")
		Sheet.write(z,2,SC)
		Sheet.write(z,3,SF)
		Sheet.write(z,4,SR)
		z+= 1
		Sheet.write(z,1,"Mittelwert")
		z+= 1
		Sheet.write(z,1,"Standardabweichung")
		z+=2
		
		

	Exceldatei.save("Auswertung_Likes.xls")
	Exceldatei.save(TemporaryFile())

def do_correlation():
	
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Korrelation")
	Sheet.write(0,0,"Category")
	Sheet.write(0,1,"Company")
	Sheet.write(0,2,"Count")
	Sheet.write(0,3,"Favorites")
	Sheet.write(0,4,"Retweets")
	cats = ["CN","A","GI","I","CS","CH","O"]
	z = 1
	for cat in cats:
		Sheet.write(z,0,cat)
		i = z
		for db in all_db:	
			x.execute(""" SELECT COUNT(Category), SUM(Favorites), SUM(Retweets) FROM """ +db+ """ WHERE Category = '""" +cat+ """' GROUP BY Category ORDER BY TimeStamp DESC""")
			result = x.fetchall()
			Sheet.write(z,1,db)
			if not result:
				Sheet.write(z,2,0)
				Sheet.write(z,3,0)
				Sheet.write(z,4,0)
			else:
				for r in result:
					Sheet.write(z,2,r[0])
					Sheet.write(z,3,r[1])
					Sheet.write(z,4,r[2])
			z += 1
		Sheet.write(z,2,"=MITTELWERT(C"+str(i)+":C"+str(z-1)+")") 
		z += 3
		

	Exceldatei.save("Korrelation.xls")
	Exceldatei.save(TemporaryFile())
	
def do_industries():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Branchenvergleich")

	Sheet.write(0,0,"Branche")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Count")
	Sheet.write(0,3,"Favorites")
	Sheet.write(0,4,"Retweets")
	Sheet.write(0,5,"Fav/Count")
	Sheet.write(0,6,"ReT/Count")
	GCN=0
	GA=0
	GGI=0
	GI=0
	GCH=0
	GCS=0
	GO=0
	GECH=0
	GECS=0
	GECN=0
	GLCN=0
	GLA=0
	GLGI=0
	GLI=0
	GLCH=0
	GLCS=0
	GLO=0
	GLECH=0
	GLECS=0
	GLECN=0
	GRCN=0
	GRA=0
	GRGI=0
	GRI=0
	GRCH=0
	GRCS=0
	GRO=0
	GRECH=0
	GRECS=0
	GRECN=0
	Gcatsv=[GCN,GA,GGI,GI,GCS,GCH,GO,GECH,GECS,GECN]
	Glikesv=[GLCN,GLA,GLGI,GLI,GLCS,GLCH,GLO,GLECH,GLECS,GLECN]
	Gretweetsv=[GRCN,GRA,GRGI,GRI,GRCS,GRCH,GRO,GRECH,GRECS,GRECN]
	z = 1
	for j, industry in enumerate(db_industry):
		CN=0
		A=0
		GI=0
		I=0
		CH=0
		CS=0
		O=0
		ECH=0
		ECS=0
		ECN=0
		LCN=0
		LA=0
		LGI=0
		LI=0
		LCH=0
		LCS=0
		LO=0
		LECH=0
		LECS=0
		LECN=0
		RCN=0
		RA=0
		RGI=0
		RI=0
		RCH=0
		RCS=0
		RO=0
		RECH=0
		RECS=0
		RECN=0
		catsv=[CN,A,GI,I,CS,CH,O,ECH,ECS,ECN]
		likesv=[LCN,LA,LGI,LI,LCS,LCH,LO,LECH,LECS,LECN]
		retweetsv=[RCN,RA,RGI,RI,RCS,RCH,RO,RECH,RECS,RECN]
		catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
		Sheet.write(z,0,industry_names[j])
		for c in industry:
			for i,cat in enumerate(catss):
				x.execute(""" SELECT Category, COUNT(Category), SUM(Favorites), SUM(Retweets) FROM """ +c+ """ WHERE Category = '"""+cat+"""' GROUP BY Category """)
				result = x.fetchall()
				for r in result:
					catsv[i]+=r[1]
					likesv[i]+=r[2]
					retweetsv[i]+=r[3]
					Gcatsv[i]+=r[1]
					Glikesv[i]+=r[2]
					Gretweetsv[i]+=r[3]

		for i in range(0,10):
			Sheet.write(z,1,catss[i])
			Sheet.write(z,2,catsv[i])
			Sheet.write(z,3,likesv[i])
			Sheet.write(z,4,retweetsv[i])
			z+=1
		z+=3
	for i in range(0,10):			
		Sheet.write(z,1,catss[i])
		Sheet.write(z,2,Gcatsv[i])
		Sheet.write(z,3,Glikesv[i])
		Sheet.write(z,4,Gretweetsv[i])
		z+=1

	Exceldatei.save("Branchen.xls")
	Exceldatei.save(TemporaryFile())


def single_tweets(industry):
	z = 1
	catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Branchenvergleich")
	Sheet.write(0,0,"Companie")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Favorites")
	Sheet.write(0,3,"Retweets")
	for companie in industry:
		for cat in catss:
			x.execute("""SELECT Category, Favorites, Retweets FROM """+companie+""" WHERE Category = '"""+cat+"""'""")
			result = x.fetchall()
			for r in result:
				Sheet.write(z,0,companie)
				Sheet.write(z,1,r[0])
				Sheet.write(z,2,r[1])
				Sheet.write(z,3,r[2])
				z+=1
		z+=1
	Exceldatei.save(industry_names[i]+".xls")
	Exceldatei.save(TemporaryFile())	 

def do_lrt_ts():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Branchenvergleich")
	Sheet.write(0,0,"Company")
	Sheet.write(0,1,"First Tweet")
	Sheet.write(0,2,"Last Tweet")
	Sheet.write(0,3,"Days Between")
	Sheet.write(0,4,"Tweets per Day")
	z=1
	for db in all_db:
		Sheet.write(z,0,db)
		x.execute("""SELECT MIN(TimeStamp), MAX(TimeStamp), COUNT(*) FROM """+db+""" WHERE Category != 'null' AND Category != 'RT'""")
		result = x.fetchall()
		for r in result:
			Sheet.write(z,1,str(r[0]))
			Sheet.write(z,2,str(r[1]))
			Sheet.write(z,5,r[2])
			z+=1
	Exceldatei.save("TimeStampTest.xls")
	Exceldatei.save(TemporaryFile())	 

def do_all():
	catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Branchenvergleich")
	Sheet.write(0,0,"Companie")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Favorites")
	Sheet.write(0,3,"Retweets")
	#cata =[]
	#catb =[]
	#coma =[]
	#comb =[]
	#inda =[]
	#indb =[]
	#gesa =[]
	#gesb =[]
	z=1
	#m=1

	for industry in db_industry:
		for companie in industry:
			#Sheet.write(m,5,companie)
			#n=m
			for cat in catss:
				x.execute("""SELECT Category, Favorites, Retweets FROM """+companie+""" WHERE Category = '"""+cat+"""'""")
				result = x.fetchall()
				#Sheet.write(m,6,cat)
				#m+=1
				for r in result:
					Sheet.write(z,0,companie)
					Sheet.write(z,1,r[0])
					Sheet.write(z,2,r[1])
					Sheet.write(z,3,r[2])
					z+=1
					#cata.append(r[1])
					#catb.append(r[2])
					#coma.append(r[1])
					#comb.append(r[2])
					#inda.append(r[1])
					#indb.append(r[2])
					#gesa.append(r[1])
					#gesb.append(r[2])
				#Sheet.write(n,7,str(scipy.stats.pearsonr(coma,comb)))
				#n+=1
			#Sheet.write(1,8,str(scipy.stats.pearsonr(coma,comb)))
			#print len(coma)
			#coma=[]
			#comb=[]
		#Sheet.write(1,9,str(scipy.stats.pearsonr(inda,indb)))
		#print len(inda)
		#inda =[]
		#indb =[]
		
	#Sheet.write(1,10,str(scipy.stats.pearsonr(gesa,gesb)))
	#print len(gesa)	
			
	Exceldatei.save("ALL.xls")
	Exceldatei.save(TemporaryFile())

def kategorien_summiert():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Auswertung")

	Sheet.write(0,0,"Company")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Count")
	Sheet.write(0,3,"Favorites")
	Sheet.write(0,4,"Retweets")
	Sheet.write(0,5,"Fav/Count")
	Sheet.write(0,6,"ReT/Count")
	catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
	z = 1
	for cat in catss:
		SC = 0
		SF = 0
		SR = 0
		for db in all_db:
			x.execute(""" SELECT Category, COUNT(Category), SUM(Favorites), SUM(Retweets) FROM """ +db+ """ WHERE Category = '"""+cat+"""' ORDER BY Count(Category) DESC""")
			result = x.fetchall()
			Sheet.write(z,0,db)
			for r in result:
				if r[1] == 0:
					Sheet.write(z,1,cat)
					Sheet.write(z,2,0)
					Sheet.write(z,3,0)
					Sheet.write(z,4,0)
					z+=1
				else:
					Sheet.write(z,1,r[0])
					Sheet.write(z,2,r[1])
					Sheet.write(z,3,r[2])
					Sheet.write(z,4,r[3])
					SC+=r[1]
					SF+=r[2]
					SR+=r[3]
					z += 1
		Sheet.write(z,1,"Summe")
		Sheet.write(z,2,SC)
		Sheet.write(z,3,SF)
		Sheet.write(z,4,SR)
		z+= 1
		Sheet.write(z,1,"Mittelwert")
		z+= 1
		Sheet.write(z,1,"Standardabweichung")
		z+=2
		
		

	Exceldatei.save("Auswertung_Likes_Kategorien2.xls")
	Exceldatei.save(TemporaryFile())
	
def verteilung_likes_rts():
	catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Branchenvergleich")
	Sheet.write(0,0,"Likes")
	Sheet.write(0,1,"Anzahl Tweets")
	Sheet.write(0,3,"RTs")
	Sheet.write(0,4,"Anzahl Tweets")
	Likes={}
	RT={}
	i=1
	sp=7
	for industry in db_industry:
		brancheLikes={}
		brancheRT={}	
		for companie in industry:
			x.execute("""SELECT Category,Favorites, Retweets FROM """+companie+""" WHERE Category != 'null' AND Category != 'RT'""")
			result = x.fetchall()
			for r in result:
				if r[1] in Likes:
					Likes[r[1]]+=1
				else:
					Likes[r[1]]=1
				if r[1] in brancheLikes:
					brancheLikes[r[1]]+=1
				else:					
					brancheLikes[r[1]]=1
				if r[2] in RT:
					RT[r[2]]+=1
				else:
					RT[r[2]]=1
				if r[2] in brancheRT:
					brancheRT[r[2]]+=1
				else:
					brancheRT[r[2]]=1
		Sheet.write(0,sp-1,industry)
		for key in brancheLikes:
			Sheet.write(i,sp,key)
			Sheet.write(i,sp+1,brancheLikes[key])
			i+=1
		i=1
		sp+=3
		for key in brancheRT:
			Sheet.write(i,sp,key)
			Sheet.write(i,sp+1,brancheRT[key])
			i+=1
		i=1
		sp+=4
	for key in Likes:
		Sheet.write(i,0,key)
		Sheet.write(i,1,Likes[key])
		i+=1
	i=1
	for key in RT:
		Sheet.write(i,3,key)
		Sheet.write(i,4,RT[key])
		i+=1
	Exceldatei.save("Verteilung Likes und RTs inklusive Branchen.xls")
	Exceldatei.save(TemporaryFile())

def Links_pro_Kategorie():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Auswertung")

	Sheet.write(0,0,"Company")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Anzahl Links")
	catss=["CN","A","GI","I","CS","CH","O","ECH","ECS","ECN"]
	z = 1
	for cat in catss:
		SL = 0
		for db in all_db:
			x.execute(""" SELECT Category, COUNT(Links) FROM """ +db+ """ WHERE Category = '"""+cat+"""' AND Links != "" ORDER BY Count(Category) DESC""")
			result = x.fetchall()
			Sheet.write(z,0,db)
			for r in result:
				if r[1] == 0:
					Sheet.write(z,1,cat)
					Sheet.write(z,2,0)
					z+=1
				else:
					Sheet.write(z,1,r[0])
					Sheet.write(z,2,r[1])
					SL+=r[1]
					z += 1
		Sheet.write(z,1,"Summe")
		Sheet.write(z,2,SL)
		z+= 1
		

	Exceldatei.save("Links_pro_kategorie.xls")
	Exceldatei.save(TemporaryFile())
	
	
def Links_pro_Unternehmen():
	Exceldatei = xlwt.Workbook()
	Sheet = Exceldatei.add_sheet("Auswertung")

	Sheet.write(0,0,"Company")
	Sheet.write(0,1,"Category")
	Sheet.write(0,2,"Likes")


	z = 1
	for db in all_db:
		SL = 0
		x.execute(""" SELECT Category, COUNT(Links) FROM """ +db+ """ WHERE Category != "null" AND Category != "RT" AND Links != "" GROUP BY Category ORDER BY Count(Category) DESC""")
		result = x.fetchall()
		Sheet.write(z,0,db)
		for r in result:
			Sheet.write(z,1,r[0])
			Sheet.write(z,2,r[1])
			SL += r[1]	
			z+=1
		Sheet.write(z,1,"Summe")
		Sheet.write(z,2,SL)
		z+= 2
		
		

	Exceldatei.save("Auswertung_Links.xls")
	Exceldatei.save(TemporaryFile())

kategorien_summiert()	
"""test ={1:10}
a=2
if a in test:
	test[1]+=1
else:
	test[a]=1
print test"""
