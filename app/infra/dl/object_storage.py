import json
import os
from core.interfaces.object_store import IObjectStore
from infra.db.connection import dl_connection

class ObjectStore(IObjectStore):

    def __init__(self, dl_client=dl_connection):
        self.dl_client = dl_client

    def insert_dl_resume(self, cpf, resume, file_extension):
        if file_extension == 'xml':
            folder = 'lattes'
            file_content = resume
        elif file_extension == 'json':
            folder = 'dgp'
            file_content = json.dumps([curso.__dict__ for curso in resume], ensure_ascii=False)
        
        if file_content:
            file_name = f"./app/infra/storage/data/{cpf}.{file_extension}"
            object_name = f"raw/{folder}/{cpf}.{file_extension}"

            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(file_content)
            
            try:
                self.dl_client.fput_object(
                    "vitae",
                    object_name,
                    file_name,
                    content_type=f'application/{file_extension}'
                )
            except ValueError as e:
                print(f"ERROR: {e}")

            os.remove(file_name)
    
    def list_dl_objects(self, bucket_name, prefix):
        objects = self.dl_client.list_objects(bucket_name, prefix=prefix, recursive=True)
        return [obj.object_name for obj in objects]
    
    def get_dl_object(self, bucket_name, object_name):
        response = self.dl_client.get_object(bucket_name, object_name)
        content = response.read()
        return json.loads(content.decode('utf-8'))
    