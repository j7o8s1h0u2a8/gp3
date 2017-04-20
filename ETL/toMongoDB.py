# Connect to MongoDB and insesrt data
# Build by Tea

from pymongo import MongoClient
import pymongo

client = MongoClient('10.120.28.55', 27017)
db = client['news']
collection = db['news']

