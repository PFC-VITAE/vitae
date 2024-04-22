from abc import ABC, abstractmethod

class IVitaeExtractor(ABC):

    @abstractmethod
    def getID(self, full_name, birth_date, cpf):
        pass

    @abstractmethod
    def getVitae(self, id):
        pass
