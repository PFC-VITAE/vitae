from core.interfaces.vitae_extractor import IVitaeExtractor
from core.interfaces.candidate_repository import ICandidateRepository
from core.interfaces.object_store import IObjectStore
from datetime import datetime
import xml.etree.ElementTree as ET

class ConsolidateCandidateData:

    def __init__(self, vitae_extractor: IVitaeExtractor, candidate_repository: ICandidateRepository, object_storage: IObjectStore):
        self.__vitae_extractor = vitae_extractor 
        self.__candidate_repository = candidate_repository
        self.__object_storage: object_storage

    def get_candidates_personal(self):
        return self.__candidate_repository.get_all_personal_info()

    def extract_resume(self, object):

        id = self.__vitae_extractor.get_ID(cpf=object.cpf, full_name=object.full_name, birth_date=object.birth_date)

        if id:
            curriculo = self.__vitae_extractor.get_vitae(id)
            return curriculo

        
    def get_all_candidates(self):
        return self.__candidate_repository.get_all_candidates()

    def extract_resume_id(self, resume_xml):
        if resume_xml: 
            root = ET.fromstring(resume_xml)
            resume_id = root.attrib.get('NUMERO-IDENTIFICADOR')
            return resume_id
        
        return None
        
    def execute(self):
        try:
            candidates_data = self.get_all_candidates()

            if len(candidates_data) < 1 or candidates_data[0].updated_last < datetime.now().year:

                candidates_list = self.get_candidates_personal()

                consolidated_candidates = []
                count = 0

                for candidate in candidates_list:
                    resume = self.extract_resume(candidate)
                    candidate.updated_last = datetime.now().year
                    candidate.resume_id = self.extract_resume_id(resume)

                    self.__object_storage.insert_dl_resume(cpf=candidate.cpf, resume=resume, file_extension='xml')
                    self.__object_storage.insert_dl_resume(cpf=candidate.cpf, resume=candidate.dgp_courses, file_extension='json')

                    if hasattr(candidate, 'dgp_courses'):
                        del candidate.dgp_courses

                    consolidated_candidates.append(candidate)
                    count += 1

                self.__object_storage.insert_candidates(consolidated_candidates)    

                return f"{count} candidates updated"
            
            else: return "All candidates are up to date"

        except ValueError as e:
            print(f"ERROR: {e}")

        

        
        


        
