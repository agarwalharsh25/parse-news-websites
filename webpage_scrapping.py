import urllib2
import re
import requests
from bs4 import BeautifulSoup
import datetime
from time import strftime
import json

def fetchNewsArticles(html):
    soup = BeautifulSoup(html, "html5lib")

    flag=0
    results = soup.find_all('div', attrs={"class":"content"})
    if len(results)!=0:
	    for res in results:
	    	if len(res.find_all('span', attrs={"class":"title"}))==0:
	    		flag=1
	    		break
    		title = res.find('span', attrs={"class":"title"}).text.replace("\n", "")
	    	if res.find("span", {"class":"meta"}).has_attr('rodate'):
	    		publishDate = res.find("span", {"class":"meta"})['rodate']
	    		publishDate = datetime.datetime.strptime(publishDate, '%Y-%m-%dT%H:%M:%SZ').strftime('%d %b %Y')
	    	else:
	    		publishDate = res.find("span", {"class":"meta"}).text
	    	link = "https://timesofindia.indiatimes.com"+res.find("a")['href']
	    	# print title+link
	    	# print publishDate
	    	d={}
	    	d['title']=title
	    	d['link']=link
	    	d['publishDate']=publishDate
	    	lst.append(d)
	    	print(d)
	    if flag==0:
	    	return 1
    
    flag=1
    results = soup.find_all('span', attrs={"class":"w_tle"})
    if len(results)!=0:
	    for res in results:
    		if res.find("a").has_attr('title'):
	    		title = res.find("a")['title'].replace("\n", "")
	    	else:
	    		flag=2
	    		break
	    	if res.next_sibling is None:
	    		break
	    	if res.next_sibling.find("span", {"class":"art_date"}).has_attr('rodate'):
	    		publishDate = res.next_sibling.find("span", {"class":"art_date"})['rodate']
	    		publishDate = datetime.datetime.strptime(publishDate, '%d %b %Y, %H:%M').strftime('%d %b %Y')
	    	link = "https://timesofindia.indiatimes.com"+res.find("a")['href']
	    	d={}
	    	d['title']=title
	    	d['link']=link
	    	d['publishDate']=publishDate
	    	lst.append(d)
	    	print(d)
	    if flag==1:
	    	return 1
    return -1

def fetchNewsArticlesEtimes(html):
    soup = BeautifulSoup(html, "html5lib")

    flag=2
    results = soup.find_all('li', attrs={"class":"md_news_box"})
    if len(results)!=0:
    	for res in results:
    		if len(res.find_all('p'))==0:
    			flag=3
    			break
    		title = res.find('p').text.replace("\n", "")
    		publishDate=""
    		link = "https://timesofindia.indiatimes.com"+res.find("a")['href']
    		d={}
	    	d['title']=title
	    	d['link']=link
	    	d['publishDate']=publishDate
	    	lst.append(d)
	    	print(d)
    	if flag==2:
    		return 1
	return -1

query = raw_input("Enter topic name ")
query = query.replace(' ', '-')
i=1
lst = []
while 1<11:
	response = urllib2.urlopen('https://timesofindia.indiatimes.com/topic/'+query+'/news/'+str(i))
	html = response.read()
	if fetchNewsArticles(html) == -1:
		break
	i = i+1
if i == 1:
	response = urllib2.urlopen('https://timesofindia.indiatimes.com/topic/'+query+'/news/')
	html = response.read()
	fetchNewsArticlesEtimes(html)

print json.dumps(lst)