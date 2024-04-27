from core.interfaces.candidate_repository import ICandidateRepository
from ..db.dto.candidate_dto import CandidateDTO
from infra.db.connection import connection

class CandidateRepository(ICandidateRepository):

    def __init__(self, client=connection):
        self.client = client

    def get_all(self):
        db = self.client["DGP_mock"]  
        collection = db["dados_pessoais"]  
        documents = list(collection.find())

        candidates_data = [CandidateDTO.from_dict(doc) for doc in documents]

        return candidates_data