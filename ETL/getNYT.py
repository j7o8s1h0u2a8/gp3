# Get NewYorkTimes news
# Build by Tea

from bs4 import BeautifulSoup
import lxml
import requests as r
import datetime as d
import pymysql
import sys
import re

# Get article list from daily news, give a date in yyyy/mm/dd format
def getDailyArticles(date):

    articlesList = []

    daily_url = 'http://www.nytimes.com/indexes/%s/todayspaper/index.html' % (
        date)

    res = r.get(daily_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    articles = soup.select('.aColumn h6 a') + soup.select(
        '.aColumn h3 a') + soup.select('#SpanABMiddleRegion h6 a')

    for article in articles:
        art_dict = {}

        art_dict['title'] = article.text.strip()
        art_dict['source'] = 'NYT'
        art_dict['url'] = article['href']
        articlesList.append(art_dict)

    return articlesList


# Get urls list of x days ... range(-x,0)
def getArticlesList(nDays):

    articlesList = []

    for delta in range(0, nDays):

        date = (d.date.today() - d.timedelta(delta)).strftime('%Y/%m/%d')
        daily_url = 'http://www.nytimes.com/indexes/%s/todayspaper/index.html' % (
            date)

        res = r.get(daily_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        articles = soup.select('.aColumn h6 a') + soup.select(
            '.aColumn h3 a') + soup.select('#SpanABMiddleRegion h6 a')

        for article in articles:
            art_dict = {}

            art_dict['title'] = article.text.strip()
            art_dict['date'] = date
            art_dict['source'] = 'NYT'
            art_dict['url'] = article['href']
            articlesList.append(art_dict)

    return articlesList


# Get a signle article content
def getArticle(art_url):

    art_dict = {}

    res = r.get(art_url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        art_date = soup.select('.dateline')[0]['content'].split('T')[0]
    except:
        art_date = d.datetime.today().strftime('%Y/%m/%d')

    art_title = soup.title.text.split(' - ')[0].strip()
    art_body = soup.select('.story-body-text')

    art_paras = {}
    for numPara in range(len(art_body)):
        para = re.sub("[“”’]",'\'', art_body[numPara].text.strip())
        art_paras[str(numPara + 1)] = para

    art_dict['title'] = art_title
    art_dict['date'] = art_date
    art_dict['source'] = 'NYT'
    art_dict['url'] = art_url
    art_dict['content'] = art_paras

    return art_dict


# Get connection to MySQL@10.120.28.52
# Get NYT article list and insert to cklist
def listToMySQL():

    # Connect to MySQL
    try:
        conn = pymysql.connect(host='127.0.0.1',
                               user='root',
                               password='m123456',
                               db='gp3',
                               charset='utf8',
                               autocommit=True,
                               cursorclass=pymysql.cursors.DictCursor)
        c = conn.cursor()
    except:
        print('Cannot connect to MySQL server!')

    # Get list and insert to gp3.cklist
    date = (d.date.today()).strftime('%Y/%m/%d')

    articles = getDailyArticles(date)
    okcount = 0
    ngcount = 0

    for article in articles:
        try:
            c.execute(
                """INSERT INTO cklist(title,source,url) VALUES (%(title)s,%(source)s,%(url)s)""", article)
            print('Insert successful: %s' % (article['url']))
            okcount += 1
        except:
            print('%s Error: %s' % (sys.exc_info()[0], article['url']))
            ngcount += 1
    print('Inserted OK:%s ; NG:%s' % (okcount, ngcount))
