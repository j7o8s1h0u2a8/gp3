import sys
import pymysql
import datetime as d

import getNYT as gn


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


# Get NYT article list
date = (d.date.today()).strftime('%Y/%m/%d')

articles = gn.getDailyArticles(date)
okcount = 0
ngcount = 0

for article in articles:
    try:
        c.execute("""INSERT INTO cklist(title,source,url) VALUES (%(title)s,%(source)s,%(url)s)""",article)
        print('Insert successful: %s'%(article['url']))
        okcount += 1
    except:
        print('%s Error: %s'%(sys.exc_info()[0],article['url']))
        ngcount += 1
print('OK:%s ; NG:%s'%(okcount,ngcount))