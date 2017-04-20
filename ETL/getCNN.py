# Get CNN news
# Build by Tea

from bs4 import BeautifulSoup
import lxml
import requests as r
import datetime as d


# Get all category links
def getCatLinks():
    main_url = 'http://edition.cnn.com/'
    res = r.get(main_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')
    tags = soup.select('.m-footer__bucket_group .m-footer__link')

    catList = []
    for tag in tags:
        if (tag['href'].split('.')[0] == '//money'):
            catList.append('http:%s' % (tag['href']))
        elif (tag['href'].split(':')[0] != 'http'):
            catList.append(main_url + '%s' % (tag['href'].lstrip('/')))
    return catList


#[DEBUG for getCatLinks()]
# for link in getCatLinks():
#     res = r.get(link)
#     if res.status_code == 200:
#         print('[ok!]' + link)
#     else:
#         print('[%s Fail!]' % (res.status_code) + link)


# Get all article links under the given category url
def getArticlesList(cat_url):

    articlesList = []

    res = r.get(cat_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')
    titles = soup.select('.cd__headline a')

    for article in titles:
        art_info = {}
        art_info['title'] = article.text
        art_info['source'] = 'CNN'

        if (article['href'].lstrip('/').split(':')[0] == 'https'):
            art_info['url'] = article['href'].lstrip('/')
        elif (article['href'].lstrip('/').split(':')[0] == 'http'):
            art_info['url'] = article['href'].lstrip('/')
        else:
            art_info['url'] = 'http://edition.cnn.com/' + \
                article['href'].lstrip('/')

        articlesList.append(art_info)

    return articlesList

#[DEBUG for getArticlesList()]
# for catLink in getCatLinks()[0:1]:
#     print(len(getArticlesList(catLink)))

#     for art in getArticlesList(catLink):
#         res = r.get(art['url'])
#         if res.status_code == 200:
#             print('[ok!]' + art['title'])
#         else:
#             print('[%s Fail!]' % (res.status_code) + art['url'])


# Get one single article content
def getArticle(art_url):

    art_dict = {}

    res = r.get(art_url)
    res.encoding = 'unicode'
    soup = BeautifulSoup(res.text, 'lxml')

    try:
        art_date = soup.find(itemprop='datePublished')['content'].split('T')[0]
    except:
        art_date = d.date.today().strftime('%Y/%m/%d')

    art_title = soup.select('title')[0].text
    art_body = soup.select('#body-text .zn-body__paragraph')

    art_paras = {}
    for numPara in range(len(art_body)):
        art_paras[str(numPara+1)] = art_body[numPara].text.strip()

    art_dict['title'] = art_title
    art_dict['url'] = art_url
    art_dict['source'] = 'CNN'
    art_dict['date'] = art_date
    art_dict['content'] = art_paras

    return art_dict
