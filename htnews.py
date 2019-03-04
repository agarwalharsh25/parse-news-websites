import urllib2
import re
import requests
from bs4 import BeautifulSoup
import datetime
from time import strftime
import json
from HTMLParser import HTMLParser

def fetchNewsArticles(html):
    soup = BeautifulSoup(html, "html5lib")
    results = soup.find_all('span', attrs={"class":"powered-txt"})
    if len(results)!=0:
    	for res in results:
    		if res.text == ' No results found':
    			return -1
    searchNews = soup.find('div', attrs={"class":"searchNews"})
    news = searchNews.find_all('div', attrs={"class":"media-body"})
    if len(results)!=0:
	    for res in news:
	    	title = res.find('div', attrs={"class":"media-heading headingfour"}).text
	    	title = title.replace("\n", " ")
	    	title = title.replace("\t", " ")
	    	publishDate = res.find('span', attrs={"class":"time-dt"}).text
	    	try:
	    		publishDate = datetime.datetime.strptime(publishDate, '%b %d, %Y %H:%M').strftime('%d %b %Y')
	    	except ValueError as e:
	    		publishDate = datetime.datetime.strptime(publishDate, '%b %d, %Y %H:%M IST').strftime('%d %b %Y')
	    	link = res.find('div', attrs={"class":"media-heading headingfour"}).find('a')['href']
	    	d={}
	    	d['title']=HTMLParser().unescape(title)
	    	d['link']=link
	    	d['publishDate']=publishDate
	    	lst.append(d)
	    	print(d)
    return 1

query = raw_input("Enter topic name ")
query = query.replace(' ', '-')
i=1
lst = []
while 1<11:
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	site = 'https://www.hindustantimes.com/search?q='+query+'&pageno='+str(i)
	req = urllib2.Request(site, headers=hdr)
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	html = response.read()
	if fetchNewsArticles(html) == -1:
		break
	i = i+1

print json.dumps(lst)