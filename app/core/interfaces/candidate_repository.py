from abc import ABC, abstractmethod

class ICandidateRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass