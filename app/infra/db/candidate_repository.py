from core.interfaces.candidate_repository import ICandidateRepository
from ..db.dto.candidate_dto import CandidateDTO
from infra.db.connection import connection
from core.entities.candidate import Candidate
from infra.helpers.dict_to_object import dict_to_object

class CandidateRepository(ICandidateRepository):

    def __init__(self, client=connection):
        self.client = client

    def get_all_personal_info(self):
        db = self.client["DGP_mock"]  
        collection = db["personal_data"]  
        documents = list(collection.find())

        candidates_data = [CandidateDTO.from_dict(doc) for doc in documents]

        return candidates_data
    
    def insert_candidates(self, candidates_list):
        db = self.client["vitae"]
        collection = db["candidate_lattes"]

        candidates_dict_list = [candidate.to_dict() for candidate in candidates_list]

        data = collection.insert_many(candidates_dict_list)

        return data        

    def get_all_candidates(self):
        db = self.client["vitae"]
        collection = db["candidate_lattes"]
        documents = list(collection.find())

        candidates_data = [Candidate(dict_to_object(doc)) for doc in documents]

        return candidates_data
