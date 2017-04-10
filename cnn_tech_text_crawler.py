import re
import requests
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


def tech_text(lines):
    x = ''
    for i in lines:
        try:
            html = urlopen(i)
            soup = BeautifulSoup(html, 'lxml')
            a = soup.find('div', {"id": "storytext"}).findAll("p")
            for j in a:
                m = j.text.replace('(', '').replace(')', '').replace('\\', '').replace(',', '').replace('.', '').replace('"','').replace('?', '').replace('-', '').replace('\n', '')
                x+=m+"\n"
            write_file(x)
            x=''
        except:
            pass
def write_file(m):
    global i
    f = open('e://cnn_tech_text/cnn_tech_text_{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H')+'_'+str(i)),'a',encoding='utf-8')
    f.write(m)
    i+=1


i = 1
list_url=[]
f = open('e://3345678/cnn_tech_url_{}.txt'.format(datetime.datetime.now().strftime('%Y_%m_%d_%H')),'rt')
lines = f.readlines()
tech_text(lines)
