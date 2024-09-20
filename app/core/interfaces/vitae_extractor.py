from abc import ABC, abstractmethod


class IVitaeExtractor(ABC):

    @abstractmethod
    def get_ID(self, full_name, birth_date, cpf):
        pass

    @abstractmethod
    def get_vitae(self, id):
        pass
