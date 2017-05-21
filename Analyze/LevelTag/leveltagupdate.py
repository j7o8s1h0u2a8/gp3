import pymongo


conn = pymongo.MongoClient('10.120.28.55',27017)
db = conn['news']
DB_news = db['news']
DB_art_keywords = db['art_keywords']

count = 1
articles = DB_art_keywords.find()
for article in articles:
    DB_news.find_one_and_update({'_id':article['_id'],'keywords':{'$exists':False}},{'$set':{'keywords':article['keywords']}})
    print(count,'updated')
    count +=1