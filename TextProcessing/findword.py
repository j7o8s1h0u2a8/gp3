import pymongo

# Get connection to MongoDB@10.120.28.55
try:
    client = pymongo.MongoClient('10.120.28.55', 27017)
    db = client['news']
    DB_news = db['news']
except:
    print('Cannot connect to MongoDB server!')


# 查詢某生詞出處
findid = 'wordset.'+ 'dcdcdcd'
result = DB_news.find_one({findid:{'$exists':True}})
#     print('art_id:%s,para_id:%s'%(result['_id'], result['wordset'][userinput]['from']))

if str(result) == 'None':
	print('44')

# para_id = result['wordset']['dcdcdcd']['from'][0]
# para = result['content'][para_id]


# print(para)