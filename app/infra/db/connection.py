import urllib.parse
from pymongo import MongoClient
from ..config import *

dgp_username = urllib.parse.quote_plus(dgp_mongo_db_user)
dgp_password = urllib.parse.quote_plus(dgp_mongo_db_password)
dgp_cluster = urllib.parse.quote_plus(dgp_mongo_db_cluster)
dgp_connection = MongoClient(
    "mongodb+srv://%s:%s@%s.2gabpap.mongodb.net/"
    % (dgp_username, dgp_password, dgp_cluster)
)

db_username = urllib.parse.quote_plus(mongo_local_user)
db_password = urllib.parse.quote_plus(mongo_local_password)
db_connection = MongoClient(
    "mongodb://%s:%s@%s/" % (db_username, db_password, mongo_local_url)
)
