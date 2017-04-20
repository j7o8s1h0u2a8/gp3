# Get NewYorkTimes news
# Build by Tea

from bs4 import BeautifulSoup
import lxml
import requests as r
import datetime as d


# Get urls list of x days ... range(-x,0)
def getArticlesList(nDays):

    articlesList = []

    for delta in range(90, nDays):

        date = (d.date.today() - d.timedelta(delta)).strftime('%Y/%m/%d')
        daily_url = 'http://www.nytimes.com/indexes/%s/todayspaper/index.html' % (date)

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
        art_paras[str(numPara + 1)] = art_body[numPara].text.strip()

    art_dict['title'] = art_title
    art_dict['date'] = art_date
    art_dict['source'] = 'NYT'
    art_dict['url'] = art_url
    art_dict['content'] = art_paras

    return art_dict
