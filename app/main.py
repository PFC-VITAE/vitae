from core.usecases.consolidate_candidate_data import ConsolidateCandidateData
from infra.db.candidate_repository import CandidateRepository
from infra.services.vitae_extractor import VitaeExtractor

if __name__ == "__main__":

    repository = CandidateRepository()
    vitae_extrator = VitaeExtractor()

    usecase_consolidate_candidate_data = ConsolidateCandidateData(candidate_repository=repository, vitae_extractor=vitae_extrator)
    
    result = usecase_consolidate_candidate_data.execute()

    print(result)