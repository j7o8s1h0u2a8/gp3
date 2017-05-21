import pymongo
import math
import operator
import multiprocessing
import time



# 輸入兩 collections, 計算總篇數 N & 更新 word_dict中 IDF值
def updateIDF(N, DB_word_dict):
    word_dict = DB_word_dict.find()
    for word in word_dict:
        idf = math.log(N/word['count'])
        DB_word_dict.update_one({'_id': word['_id']}, {'$set': {'IDF': idf}})
    print('IDF in DB_word_dict updated.')


# Input一篇文章，與 DB_word_dict比對該文章 wordset裡的字詞
# 計算該文章 wordset的 TFIDF，排序取前 10獲得 keywords dict
def findkeywords(wordset, DB_word_dict):
    tfidf_dict = {}
    for word in wordset['wordset']:
        ref = DB_word_dict.find_one({'_id':word})
        try:
            tfidf = wordset['wordset'][word]['TF']*ref['IDF']
            tfidf_dict[word] = tfidf
        except TypeError:
            DB_art_keywords.find_one_and_update({'_id':wordset['_id']}, {'$unset':{word:1}})
    kw_TFIDF = sorted(tfidf_dict.items(), key=operator.itemgetter(1), reverse=True)[0:10]
    return dict(kw_TFIDF)



connection = pymongo.MongoClient('127.0.0.1',27017)
db = connection['MyTest']
DB_art_keywords = db['art_keywords']
DB_word_dict = db['word_dict']

# 更新IDF
# N = DB_art_keywords.find().count()
# updateIDF(N, DB_word_dict)

# wordsets = DB_art_keywords.find_one({'keywords':{'$exists':False}})
# wordsets = DB_art_keywords.find_one_and_update({'keywords': {'$exists': False}},{'$set':{'keywords':'Processing...'}})
wordsets = DB_art_keywords.find({'keywords': {'$exists': False}}, {'_id':1, 'wordset':1})
count = 1

for wordset in wordsets:
    kw_TFIDF = findkeywords(wordset, DB_word_dict)
    DB_art_keywords.update_many({'_id':wordset['_id']}, {'$set':{'keywords':kw_TFIDF}}, upsert=True)
    print(count, wordset['_id'], ' is updated keywords!')
    count += 1
