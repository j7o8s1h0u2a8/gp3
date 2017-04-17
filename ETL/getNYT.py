
# coding: utf-8

# In[1]:

get_ipython().system('pip install requests')
get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')


# In[2]:

from bs4 import BeautifulSoup
import lxml
import requests as r
import json
from datetime import date
from datetime import timedelta
import json


# In[23]:

#Get urls list of x days ... range(-x,0)
def getArticleList(nDays):
    
    articleList = []
    
    for delta in range(-nDays,0):
        
        day = date.today() + timedelta(delta)
        daily_url = 'http://www.nytimes.com/indexes/' + day.strftime('%Y/%m/%d') + '/todayspaper/index.html'
        
        res = r.get(daily_url)
        res.encoding='unicode'
        soup = BeautifulSoup(res.text,'lxml')
        articles = soup.select('#SpanABMiddleRegion h6 a')
        
        for num in range(len(articles)):
            url_dict = {}
            
            url_dict['title'] = articles[num].text.strip()
            url_dict['date'] = day.strftime('%Y/%m/%d')
            url_dict['source'] = 'NYT'
            url_dict['url'] = articles[num]['href']
            articleList.append(url_dict)

    return articleList


# In[25]:

#Get single article content
def addContent(articleList):
    
    textCollection = []    #output list
    
    for num in range(len(articleList)):
                
        res = r.get(articleList[num]['url'])
        res.encoding='unicode'
        soup = BeautifulSoup(res.text,'lxml')
        contents = soup.select('.story-body-supplemental .story-body-text.story-content')
        
        paragraph_dict = {} 
        for numPara in range(len(contents)):
            paragraph_dict[numPara+1] = contents[numPara].text.strip()
        
        article_dict = {}    #store hole article details
        article_dict['title'] = articleList[num]['title']
        article_dict['date'] = articleList[num]['date']
        article_dict['source'] = articleList[num]['source']
        article_dict['url'] = articleList[num]['url']
        article_dict['content'] = paragraph_dict
        
        textCollection.append(article_dict)
            
    return textCollection


# In[29]:

def jsonOut(dict):
    with open('contents.json', 'w') as f:
        json.dump(dict, f)


# In[30]:

#debug, choose 2 articles for test
len(getArticleList(1))
test = []
for i in range(0,2):
    test.append(getArticleList(1)[i])
addContent(test)
jsonOut(addContent(test))

