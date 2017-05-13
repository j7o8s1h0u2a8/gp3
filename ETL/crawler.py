import pymysql
from pymongo import MongoClient
import pymongo

import getNYT as gn


# Get article list and insert to MySQL
gn.listToMySQL()


# Get connection to MySQL@10.120.28.52
try:
  conn = pymysql.connect(host='10.120.28.52',
                         user='gp3',
                         password='Group_03',
                         db='gp3',
                         charset='utf8',
                         autocommit=True,
                         cursorclass=pymysql.cursors.DictCursor)
  c = conn.cursor()
except:
  print('Cannot connect to MySQL server!')


# Get connection to MongoDB@10.120.28.55
try:
  client = MongoClient('10.120.28.55', 27017)
  db = client['news']
  collection = db['news']
except:
  print('Cannot connect to Mongo server!')


# Get unread url from cklist table
records = c.execute(
    """SELECT url FROM cklist WHERE source = 'NYT' AND tag = 'N'""")
print('Get %s records.' % (records))

urls = []
for record in c:
  urls.append(record['url'])
# print(urls)


# Get article content and insert into MongoDB
okcount = 0
ngcount = 0

for url in urls:

  art_dict = gn.getArticle(url)

  # print('%s has %s paras' % (art_dict['title'], len(art_dict['content'])))

  if (len(art_dict['content']) > 1):
    collection.insert_one(art_dict)
    print('[%s paras inserted!] url: %s' %
          (len(art_dict['content']), url))
    okcount += 1
  else:
    print('\n[NG!] %s' % (art_dict['url']))
    print('The article has only %s paras.\n' % (len(art_dict['content'])))
    ngcount += 1

  c.execute("""UPDATE cklist SET tag = 'R' WHERE url = %s""", url)

print('\nCrawler finished! %s articles are inserted to MongoDB. %s are failed.\n' %
      (okcount, ngcount))
