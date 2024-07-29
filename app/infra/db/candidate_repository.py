from core.interfaces.candidate_repository import ICandidateRepository
from ..db.dto.candidate_dto import CandidateDTO
from infra.db.connection import dgp_connection, db_connection, dl_connection
from core.entities.candidate import Candidate
from infra.helpers.dict_to_object import dict_to_object
import json, os

class CandidateRepository(ICandidateRepository):

    def __init__(self, dgp_client=dgp_connection, db_client=db_connection, dl_client=dl_connection):
        self.dgp_client = dgp_client
        self.db_client = db_client
        self.dl_client = dl_client


    def get_all_personal_info(self):
        try: 
            db = self.dgp_client["DGP_mock"]  
            collection = db["personal_data"]  
            documents = list(collection.find())

            candidates_data = [CandidateDTO.from_dict(doc) for doc in documents]

            return candidates_data
        
        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco DGP") from e
    
    def insert_candidates(self, candidates_list):
        try:
            db = self.db_client["vitae"]
            collection = db["candidates"]

            candidates_dict_list = [candidate.__dict__ for candidate in candidates_list]

            for candidate in candidates_dict_list:
                candidate_id = candidate.get('_id')

                if candidate_id:
                    collection.replace_one({'_id': candidate_id}, candidate, upsert=True)


            return "Dados inseridos ou atualizados com sucesso"
              
        except Exception as e:
            raise ValueError("Erro ao inserir dados no banco") from e


    def get_all_candidates(self):
        try:
            db = self.db_client["vitae"]
            collection = db["candidates"]
            documents = list(collection.find())

            candidates_data = [(dict_to_object(doc)) for doc in documents]

            return candidates_data
        
        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco") from e
        

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
