from dotenv import load_dotenv
import os

load_dotenv()

# Variáveis de ambiente do banco de dados local do DGP
dgp_mongo_db_user = os.environ.get("DGP_MONGODB_USER")
dgp_mongo_db_password = os.environ.get("DGP_MONGODB_PASSWORD")
dgp_mongo_db_cluster = os.environ.get("DGP_MONGODB_CLUSTER")

# Endereço da VM do IME
vm_ip_addr = os.environ.get("VM_IP_ADDRESS")
vm_port = os.environ.get("VM_PORT")

# Variáveis de ambiente do banco de dados local do MongoDB
mongo_local_url = os.environ.get("MONGO_LOCAL_URL")
mongo_local_user = os.environ.get("MONGO_LOCAL_USER")
mongo_local_password = os.environ.get("MONGO_LOCAL_PASSWORD")

# Variáveis de ambiente do MinIO
minio_url = os.environ.get("MINIO_URL")
minio_access_key = os.environ.get("MINIO_ACCESS_KEY")
minio_secret_key = os.environ.get("MINIO_SECRET_KEY")
minio_bucket = os.environ.get("MINIO_BUCKET_NAME")
