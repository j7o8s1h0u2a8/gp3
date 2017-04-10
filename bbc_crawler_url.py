import requests
import re
import datetime

from bs4 import BeautifulSoup

dir = 'http://bbc.com'
dic = {'/news/':'.news.*[$1-9]','/sport/':'.sport.*[$1-9]','/weather/':'.weather.*[$1-9]','/earth/':'.earth.*[$1-9]','/capital/':'.capital.*[$1-9]','/culture/':'.culture.*.*[$1-9]'}
usr_str=''

def find_url(url,re_str):
    list_url = []
    str = ''
    url_set = set()
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for j in soup.select('a'):
        s = j.get('href')
        list_url.append(s)
    for i in list_url:
        try:
            result = re.findall(re_str, i)
            if len(result) != 0:
                str += dir + result[0]
                url_set.add(str)
                str = ''
        except:
            pass
    return url_set

def write_file(filename,str):
    f = open(filename,'w',encoding='utf-8')
    f.write(str)




for i in dic.items():
    url_news = find_url(dir+i[0],i[1])
    for j in url_news:
        usr_str+=j+'\n'
    filename = 'e://bbc_{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H') + '_'+i[0][1:len(i[0])-1])
    write_file(filename,usr_str)
    usr_str = ''