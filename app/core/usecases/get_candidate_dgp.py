from core.interfaces.candidate_repository import ICandidateRepository
from core.entities.candidate import Candidate
class GetCandidateDGP:

    def __init__(self, candidate_repository: ICandidateRepository):
        self.__candidate_repository = candidate_repository 

    def get_dgp_candidates(self):
        dgp_documents = self.__candidate_repository.get_all()

        candidates = [Candidate(doc) for doc in dgp_documents]

        return candidates
