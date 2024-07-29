from abc import ABC, abstractmethod

class ICandidateRepository(ABC):

    @abstractmethod
    def get_all_personal_info(self):
        pass

    @abstractmethod
    def insert_candidates(self, candidates_list):
        pass

    @abstractmethod
    def get_all_candidates(self):
        pass

    @abstractmethod
    def insert_dl_resume(self, cpf, resume, file_extension):
        pass