import pymongo
import re

try:
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client['news']
    DB_news = db['news']
except:
    print('Cannot connect to MongoDB server!')


def modifyContent(article):
    for para_id in article['content'].keys():
        para = article['content'][para_id]
        new_para = re.sub("[“”’]",'\'', para)
        DB_news.find_one_and_update({'_id':article['_id']},{'$set':{'content.%s'%(para_id):new_para}})
    print('%s is done'%(article['_id']))

def modifyTitle(article):
    title = article['title']
    new_title = re.sub("[“”’]",'\'', title)
    DB_news.find_one_and_update({'_id':article['_id']},{'$set':{'title':new_title}})


articles = DB_news.find().skip(41708)
count=1
for article in articles:
    modifyContent(article)
    modifyTitle(article)
    print('done:' , count)
    count+=1