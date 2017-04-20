import requests
import datetime
import re

from bs4 import BeautifulSoup

str=''
dir = 'http:'

res = requests.get('http://money.cnn.com/technology/')
soup = BeautifulSoup(res.text,'lxml')

url_set = set()
for i in soup.select('a'):
    result = re.findall('..money.cnn.com.[0-9]{4}.[0-9]{2}.[0-9]{2}.*[$index.html]', i['href'])
    if len(result)!=0:
        # list_url.append(dir+result[0])
        url_set.add(dir+result[0])

f = open('e://3345678/cnn_tech_url_{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H')),'w',encoding='utf-8')
for i in url_set:
    f.write(i+'\n')


