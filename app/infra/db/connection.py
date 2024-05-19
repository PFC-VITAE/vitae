from pymongo import MongoClient
import urllib.parse
from ..config import *

dgp_username = urllib.parse.quote_plus(dgp_mongo_db_user)
dgp_password = urllib.parse.quote_plus(dgp_mongo_db_password)
dgp_cluster = urllib.parse.quote_plus(dgp_mongo_db_cluster)
dgp_connection = MongoClient('mongodb+srv://%s:%s@%s.2gabpap.mongodb.net/' % (dgp_username, dgp_password, dgp_cluster))

db_connection = MongoClient(f"mongodb://{mongo_local_url}")


