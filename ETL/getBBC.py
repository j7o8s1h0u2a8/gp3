# Get BBC news
# Build by Tea

from bs4 import BeautifulSoup
import lxml
import requests as r
import datetime as d


# Get all category links
def getCatLinks():
    main_url = 'http://www.bbc.com/news'
    res = r.get(main_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')
    tags = soup.select('.navigation-panel__content a')

    catList = []
    for tag in tags:
        if (tag['href'].split(':')[0] != 'http'):
            catList.append('http://www.bbc.com%s' % (tag['href']))

    return catList


# Get all article links under the given category url
def getArticlesList(cat_url):

    articlesList = []

    res = r.get(cat_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')
    titles = soup.select('.title-link')

    for article in titles:
        art_info = {}
        art_info['title'] = article.text.strip()
        art_info['url'] = 'http://www.bbc.com%s' % (article['href'])
        art_info['source'] = 'BBC'

        articlesList.append(art_info)

    return articlesList


# Get one single article content
def getArticle(art_url):

    art_dict = {}

    res = r.get(art_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')

    timestamp = int(soup.select('.story-body .date')[0]['data-seconds'])
    url_date = d.datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')

    art_title = soup.select('.story-body h1')[0].text
    art_body = soup.select('.story-body__inner p')

    art_paras = {}
    for numPara in range(len(art_body)):
        art_paras[numPara + 1] = art_body[numPara].text

    art_dict['title'] = art_title
    art_dict['url'] = art_url
    art_dict['source'] = 'BBC'
    art_dict['date'] = url_date
    art_dict['content'] = art_paras

    return art_dict
