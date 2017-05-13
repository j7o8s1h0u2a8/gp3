import re
import pymongo
from bson.objectid import ObjectId
from collections import Counter
import multiprocessing
import os
from textblob import TextBlob
from textblob import Word
import time


# 定義 stopwords
def defineStopWords():
    with open('stop-word-list.txt', 'r', encoding='utf8') as mysw:
        swlist = mysw.read().split(',')
        mysw.close()
    return swlist


# 文字處理，回傳該段落內所有字 <List> parawds
def get_parawds(content, swlist):
    words = str(TextBlob(content).words.lower())
    match = re.findall('[a-z]+', words)
    myFilter = re.compile(r'(\w)\1{2,}')
    filtered = [word for word in match if not myFilter.search(word)]
    parawds= []
    for word in filtered:
        if word not in swlist and len(word) > 2:
            finalWord = Word(word).singularize().lemmatize("v")
            parawds.append(finalWord)
    return parawds


# 傳入全文字詞清單 <List> all_wds，回傳 <Dictionary> wc_dict
def wordcount(all_wds):
    wc_dict = Counter()
    for word in all_wds:
        if word not in wc_dict:
            wc_dict[word] = 1
        else:
            wc_dict[word] += 1
    return wc_dict


# 收集該字詞出現段落-不重複記 <List> src
def get_src(word, all_parawds):
    src = set([])
    for parawds in all_parawds:
        if word in parawds:
            src.add(str(all_parawds.index(parawds)+1))
    return list(src)


# 建立該字詞資料 & TF值，回傳 <Dictionary> wdinfo
def get_wdinfo(word, wc_dict, all_parawds, n):
    wdinfo = {}
    wdinfo['count'] = wc_dict[word]
    wdinfo['TF'] = wc_dict[word]/n
    wdinfo['from'] = get_src(word, all_parawds)
    return wdinfo


# 更新資料庫 DB_word_dict
def update_DB_word_dict(wordset, DB_word_dict):
    for word in wordset:
        DB_word_dict.update_one({'_id': word}, {'$inc': {'count':1}}, upsert=True)


# 更新資料庫 DB_news
def update_DB_news(art_id, wds_info, DB_news):
    DB_news.update_one({'_id': art_id}, {'$set':{'counted':'true'}}, upsert=True)
    DB_news.update_many({'_id': art_id}, {'$set':{'wordset':wds_info}}, upsert=True)


# [MAIN PROGRAM]
def wc(swlist, connection):
    info('Child Process for wc()')

    db = connection.news
    DB_news = db['news']
    DB_word_dict = db['word_dict']

    article = DB_news.find_one_and_update({'counted': {'$exists': False}},{'$set':{'counted':'Processing...'}})
    # article = DB_news.find_one({"_id" : ObjectId('59088179f5dbe30006dd1812')})
    content = article['content']
    art_id = article['_id']

    all_parawds = []
    for para_id in range(len(content)):
        try:
            parawds = get_parawds(content[str(para_id + 1)], swlist)
        except KeyError:
            parawds = []
        all_parawds.append(parawds)

    all_wds = [word for parawds in all_parawds for word in parawds]
    n = len(all_wds)
    wordset = set(all_wds)
    wc_dict = wordcount(all_wds)

    wds_info = {}
    for word in wordset:
        wds_info[word] = get_wdinfo(word, wc_dict, all_parawds, n)

    update_DB_news(art_id, wds_info, DB_news)
    update_DB_word_dict(wordset, DB_word_dict)

    connection.close()

    print('\tart_id: %s wordcount finished with %s words.' % (art_id,n))

    # message = '\tart_id: %s wordcount finished with %s words.' % (art_id,n)
    # return message    



def info(title):
    print(title,', process id:', os.getpid())
    # print('module name:', __name__)
    # print('parent process:', os.getppid())
    # print('process id:', os.getpid())

def run(swlist):
    # swlist = defineStopWords()
    connection = pymongo.MongoClient('127.0.0.1', 27017, maxPoolSize=10)
    wc(swlist, connection)


if __name__ == '__main__':
    swlist = defineStopWords()
    info('Parent Process')
    tStart = time.time()
    with multiprocessing.Pool(4) as p:
        p.map(run, [swlist for i in range(24830)])
    tEnd = time.time()
    print('Cost %f seconds.'%(tEnd-tStart))




# if __name__ == '__main__':
#     swlist = defineStopWords()
#     info('Parent Process')
#     tStart = time.time()
#     with multiprocessing.Pool(5) as p:
#         for i in range(5):
#             p.map(run(swlist))    
#     tEnd = time.time()
#     print('Cost %f seconds.'%(tEnd-tStart))
