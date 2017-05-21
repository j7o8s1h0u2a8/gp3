import csv
import pymongo
import operator


# 從關鍵字定等級
def define_level(article,mydict):
    level_dict = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
    for word in article['keywords'].keys():
        if word in mydict:
            level_dict[mydict[word]] += 1
    sorted_dict = sorted(level_dict.items(), key=operator.itemgetter(1), reverse=True)
    leveltag = sorted_dict[0][0]
    return leveltag


# 開啟等級字典
with open('vocabulary_list_new.csv', mode='r') as infile:
    reader = csv.reader(infile)
    mydict = {rows[0]:rows[1] for rows in reader}



connection = pymongo.MongoClient('localhost:27017')
db = connection['news']
DB_news = db['news']
DB_art_keywords = db['art_keywords']


articles = DB_art_keywords.find({'level':{'$exists':False}})
count=1
for article in articles:
    leveltag = define_level(article,mydict)
    # DB_news.find_one_and_update({'_id':article['_id']},{'$set':{'level':leveltag}})
    DB_art_keywords.find_one_and_update({'_id':article['_id']},{'$set':{'level':leveltag}})
    print(count, ' is updated level tag.')
    count += 1