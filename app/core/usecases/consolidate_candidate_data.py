from core.interfaces.vitae_extractor import IVitaeExtractor
from core.interfaces.candidate_repository import ICandidateRepository
from core.entities.candidate import Candidate
from datetime import datetime


class ConsolidateCandidateData:

    def __init__(self, vitae_extractor: IVitaeExtractor, candidate_repository: ICandidateRepository):
        self.__vitae_extractor = vitae_extractor 
        self.__candidate_repository = candidate_repository

    def get_candidates_personal(self):
        candidates_data = self.__candidate_repository.get_all_personal_info()

        candidates = [Candidate(doc) for doc in candidates_data]

        return candidates

    def extract_resume(self, object: Candidate):

        id = self.__vitae_extractor.get_ID(cpf=object.cpf, full_name=object.full_name, birth_date=object.birth_date)

        if id:
            curriculo = self.__vitae_extractor.get_vitae(id)
            return curriculo

        
    def get_all_candidates(self):
        return self.__candidate_repository.get_all_candidates()
        
    def execute(self):
        try:
            candidates_data = self.get_all_candidates()

            if len(candidates_data) < 1 or candidates_data[0].updated_last < datetime.now().year:

                candidates_list = self.get_candidates_personal()

                consolidated_candidates = []

                for candidate in candidates_list:
                    resume = self.extract_resume(candidate)
                    candidate.updated_last = datetime.now().year
                    candidate.resume = resume
                
                    consolidated_candidates.append(candidate)
                    
                return self.__candidate_repository.insert_candidates(consolidated_candidates)
            
            else: return candidates_data

        except ValueError as e:
            print(f"ERROR: {e}")

        

        
        


        
