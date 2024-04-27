from dotenv import load_dotenv
import os

load_dotenv()

extrator_lattes_url = os.environ.get("WSDL_EXTRATOR_LATTES")

mongo_db_user = os.environ.get("MONGODB_USER")
mongo_db_password = os.environ.get("MONGODB_PASSWORD")
mongo_db_cluster = os.environ.get("MONGODB_CLUSTER")