from core.interfaces.vitae_extractor import IVitaeExtractor

class ConsolidateCandidateData:

    def __init__(self, vitae_extractor: IVitaeExtractor):
        self.__vitae_extractor = vitae_extractor 

    def extract_vitae(self, cpf, full_name, birth_date):
        id = self.__vitae_extractor.getID(cpf=cpf, full_name=full_name, birth_date=birth_date)

        if id:
            curriculo = self.__vitae_extractor.getVitae(id)
            return curriculo
