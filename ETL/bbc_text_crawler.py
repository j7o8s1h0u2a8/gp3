from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import requests
import datetime

list_dir = ['news','sport','weather','earth','capital','culture']
dir  ='e://bbc_{}'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H')+'_')




def get_text(lines):
    text = ''
    for i in lines:
        try:
            html = urlopen(i)
            soup = BeautifulSoup(html, 'lxml')
            str = ''
            bq = soup.findAll('div', {'class': 'story-body__inner'})
            for e in soup.select("script"):
                e.extract()
            for i in soup.select("style"):
                i.extract()
            for i in bq:
                # text += i.get_text()
                print(i.get_text())
        except:
            pass
    return text
# fin = open('e://bbc_2017_04_08_09_sport.txt', 'rt')
# lines = fin.readlines()
# get_text(lines)
# fin.close()
# get_text(lines)
# #


def write_file(filename):
    fin  = open(filename,'rt')
    lines = fin.readlines()
    get_text(lines)
    fin.close()

for i in list_dir:
    url_real = dir + i + '.txt'
    write_file(url_real)
