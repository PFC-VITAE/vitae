from core.interfaces.candidate_repository import ICandidateRepository
from core.entities.candidate import Candidate

class GetCandidatePersonalInfo:

    def __init__(self, candidate_repository: ICandidateRepository):
        self.__candidate_repository = candidate_repository 

    def get_personal_info(self):
        candidates_data = self.__candidate_repository.get_all()

        candidates = [Candidate(doc) for doc in candidates_data]

        return candidates
