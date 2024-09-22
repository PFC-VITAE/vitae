from minio import Minio
from ..config import *

dl_connection = Minio(
    minio_url, access_key=minio_access_key, secret_key=minio_secret_key, secure=False
)
