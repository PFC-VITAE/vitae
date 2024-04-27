from pymongo import MongoClient
import urllib.parse
from ..config import *

username = urllib.parse.quote_plus(mongo_db_user)
password = urllib.parse.quote_plus(mongo_db_password)
cluster = urllib.parse.quote_plus(mongo_db_cluster)
connection = MongoClient('mongodb+srv://%s:%s@%s.2gabpap.mongodb.net/' % (username, password, cluster))