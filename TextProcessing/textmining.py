import nltk
# from nltk.corpus import brown
# from nltk.book import *
import json
from pprint import pprint


with open('news.news.json',encoding='utf-8') as f:
	text = json.load(f)

# pprint(text)
print(text['content'])