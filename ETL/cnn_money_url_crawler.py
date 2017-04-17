import requests
import datetime
import re

from bs4 import BeautifulSoup


dir = 'http://money.cnn.com'
res = requests.get('http://money.cnn.com/INTERNATIONAL/')
soup = BeautifulSoup(res.text,'lxml')
url_set = set()

str = ''
for i in soup.select('a'):
    try:
        result = re.findall('.[0-9]{4}.[0-9]{2}.[0-9]{2}..*[$index.html]',i['href'])
        if len(result)!=0:
            url_set.add(dir + result[0])
    except:
        pass

f = open('e://3345678/cnn_international_url_{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H')),'w',encoding='utf-8')
for i in url_set:
    f.write(i+'\n')

