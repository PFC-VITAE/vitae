from dotenv import load_dotenv
import os

load_dotenv()

dgp_mongo_db_user = os.environ.get("DGP_MONGODB_USER")
dgp_mongo_db_password = os.environ.get("DGP_MONGODB_PASSWORD")
dgp_mongo_db_cluster = os.environ.get("DGP_MONGODB_CLUSTER")

vm_ip_addr = os.environ.get("VM_IP_ADDRESS")
vm_port = os.environ.get("VM_PORT")

mongo_local_url = os.environ.get("MONGO_LOCAL_URL")