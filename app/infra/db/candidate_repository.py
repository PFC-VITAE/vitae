from core.interfaces.candidate_repository import ICandidateRepository
from ..db.dto.candidate_dto import CandidateDTO
from infra.db.connection import dgp_connection, db_connection
from core.entities.candidate import Candidate
from infra.helpers.dict_to_object import dict_to_object

class CandidateRepository(ICandidateRepository):

    def __init__(self, dgp_client=dgp_connection, db_client=db_connection):
        self.dgp_client = dgp_client
        self.db_client = db_client


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
            collection = db["consolidated_data"]

            candidates_dict_list = [candidate.to_dict() for candidate in candidates_list]

            data = collection.insert_many(candidates_dict_list)

            return data  
              
        except Exception as e:
            raise ValueError("Erro ao inserir dados no banco") from e


    def get_all_candidates(self):
        try:
            db = self.db_client["vitae"]
            collection = db["consolidated_data"]
            documents = list(collection.find())

            candidates_data = [Candidate(dict_to_object(doc)) for doc in documents]

            return candidates_data
        
        except Exception as e:
            raise ValueError("Erro ao buscar dados no banco") from e
